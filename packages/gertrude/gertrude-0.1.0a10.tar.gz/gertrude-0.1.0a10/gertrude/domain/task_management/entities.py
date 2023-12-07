# Gertrude --- GTD done right
# Copyright © 2020-2023 Tanguy Le Carrour <tanguy@bioneland.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import Any, Optional

from bl3d import Entity
from bl3d.event_sourcing import DomainEvent, EntityState
from typing_extensions import Self  # Required before Python 3.11

from .enums import TaskStates
from .events import (
    TaskActionable,
    TaskAssignedTo,
    TaskCaptured,
    TaskDelegatedTo,
    TaskDone,
    TaskEliminated,
    TaskEvent,
    TaskFiled,
    TaskIncubated,
    TaskReclaimed,
    TaskScheduled,
    TaskUpdated,
)
from .exceptions import DateInThePast, TransitionNotAllowed
from .services import Calendar
from .value_objects import Date, Description, Person, ProjectId, TaskId, Title, UserId

POSSIBLE_NEXT_STATES_OF_TASK = {
    TaskStates.CAPTURED: (
        TaskStates.ELIMINATED,
        TaskStates.FILED,
        TaskStates.INCUBATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.DONE: (),
    TaskStates.DELEGATED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.ACTIONABLE: (
        TaskStates.ELIMINATED,
        TaskStates.INCUBATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.SCHEDULED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.SCHEDULED,
    ),
    TaskStates.FILED: (),
    TaskStates.INCUBATED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.ELIMINATED: (),
}


@dataclass(frozen=True)
class TaskState(EntityState):
    id: TaskId
    state: TaskStates
    title: Title
    description: Description
    assigned_to: Optional[ProjectId] = None
    delegated_to: Optional[Person] = None
    scheduled_on: Optional[Date] = None

    def apply(self, event: DomainEvent) -> Self:
        # To make MyPy stop complaining about all `apply` calls.
        return super().apply(event)  # type: ignore

    def apply_task_captured(self, event: TaskCaptured) -> Self:
        # Should never be called as the first state is captured!
        return self.__create_new_state_with(
            task_id=TaskId(event.task_id),
            title=event.title,
            description=event.description or "",
            state=TaskStates.CAPTURED,
        )

    def apply_task_eliminated(self, event: TaskEliminated) -> Self:
        return self.__create_new_state_with(state=TaskStates.ELIMINATED)

    def apply_task_filed(self, event: TaskFiled) -> Self:
        return self.__create_new_state_with(state=TaskStates.FILED)

    def apply_task_incubated(self, event: TaskIncubated) -> Self:
        return self.__create_new_state_with(state=TaskStates.INCUBATED)

    def apply_task_done(self, event: TaskDone) -> Self:
        return self.__create_new_state_with(state=TaskStates.DONE)

    def apply_task_delegated_to(self, event: TaskDelegatedTo) -> Self:
        return self.__create_new_state_with(
            state=TaskStates.DELEGATED, delegated_to=Person(event.person)
        )

    def apply_task_reclaimed(self, event: TaskReclaimed) -> Self:
        return self.__create_new_state_with(
            state=TaskStates.ACTIONABLE, delegated_to=None
        )

    def apply_task_scheduled(self, event: TaskScheduled) -> Self:
        return self.__create_new_state_with(
            state=TaskStates.SCHEDULED,
            scheduled_on=Date.from_isoformat(event.date),
        )

    def apply_task_actionable(self, event: TaskActionable) -> Self:
        return self.__create_new_state_with(state=TaskStates.ACTIONABLE)

    def apply_task_assigned_to(self, event: TaskAssignedTo) -> Self:
        # FIXME this is not a transition!
        if self.state == TaskStates.ELIMINATED:
            raise TransitionNotAllowed(self.state, self.state)
        return self.__create_new_state_with(assigned_to=ProjectId(event.project_id))

    def apply_task_updated(self, event: TaskUpdated) -> Self:
        return self.__create_new_state_with(
            title=Title(event.title),
            description=Description(event.description),
        )

    def __create_new_state_with(self, **kwargs: Any) -> Self:
        if "state" in kwargs:
            self.__check_transition(kwargs["state"])

        return TaskState(  # type: ignore[return-value]
            self.version + 1,
            kwargs.get("task_id", self.id),
            kwargs.get("state", self.state),
            kwargs.get("title", self.title),
            kwargs.get("description", self.description),
            kwargs.get("assigned_to", self.assigned_to),
            kwargs.get("delegated_to", self.delegated_to),
            kwargs.get("scheduled_on", self.scheduled_on),
        )

    def __check_transition(self, state: TaskStates) -> None:
        if self.state not in POSSIBLE_NEXT_STATES_OF_TASK:
            raise TransitionNotAllowed(self.state, state)
        if state not in POSSIBLE_NEXT_STATES_OF_TASK[self.state]:
            raise TransitionNotAllowed(self.state, state)


class Task(Entity):
    __state: TaskState

    @classmethod
    def instanciate(cls, events: list[TaskEvent]) -> Self:
        assert events
        captured = events[0]
        assert captured.version == 1, "Captured MUST always be the first event!"
        assert isinstance(captured, TaskCaptured)

        state = TaskState(
            1,
            TaskId(captured.task_id),
            TaskStates.CAPTURED,
            Title(captured.title),
            Description(captured.description or ""),
        )
        for e in events[1:]:
            state = state.apply(e)

        return cls(state)

    def __init__(self, state: TaskState) -> None:
        self.__state = state

    def eliminate(self) -> list[DomainEvent]:
        event = TaskEliminated(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def file(self) -> list[DomainEvent]:
        event = TaskFiled(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def incubate(self) -> list[DomainEvent]:
        event = TaskIncubated(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def do(self) -> list[DomainEvent]:
        event = TaskDone(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def delegate_to(self, delegated_to: Person) -> list[DomainEvent]:
        event = TaskDelegatedTo(
            self.__state.version + 1, str(self.__state.id), str(delegated_to)
        )
        self.__state = self.__state.apply(event)
        return [event]

    def reclaim(self) -> list[DomainEvent]:
        event = TaskReclaimed(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def schedule_on(self, date: Date, calendar: Calendar) -> list[DomainEvent]:
        if date <= calendar.today():
            raise DateInThePast(date.to_date(), calendar.today().to_date())

        event = TaskScheduled(
            self.__state.version + 1, str(self.__state.id), date.format("%Y-%m-%d")
        )
        self.__state = self.__state.apply(event)
        return [event]

    def mark_as_actionable(self) -> list[DomainEvent]:
        event = TaskActionable(self.__state.version + 1, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def assign_to(self, assigned_to: ProjectId) -> list[DomainEvent]:
        events: list[DomainEvent] = []

        event: DomainEvent = TaskAssignedTo(
            self.__state.version + 1, str(self.__state.id), str(assigned_to)
        )
        self.__state = self.__state.apply(event)
        events.append(event)

        # If it's assigned to a project, it means the project already
        # exists and contains tasks, so chances are this newly captured task
        # is not the very next thing to be done.
        if self.__state.state == TaskStates.CAPTURED:
            event = TaskIncubated(self.__state.version + 1, str(self.__state.id))
            self.__state = self.__state.apply(event)
            events.append(event)

        return events

    def update(self, title: Title, description: Description) -> list[DomainEvent]:
        if self.__state.title == title and self.__state.description == description:
            return []

        event = TaskUpdated(
            self.__state.version + 1, str(self.__state.id), str(title), str(description)
        )
        self.__state = self.__state.apply(event)
        return [event]


class User:
    def __init__(self, identifier: UserId) -> None:
        self.__identifier = identifier
