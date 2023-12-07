# Gertrude --- GTD done right
# Copyright © 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

import datetime
from abc import ABC, abstractmethod

from bles import Projector, ProjectorTypes

from gertrude.domain.task_management.enums import TaskStates


class TaskProjection(ABC):
    @abstractmethod
    def capture(self, task_id: str, user_id: str, title: str, description: str) -> None:
        ...

    @abstractmethod
    def update_state(self, task_id: str, state: str) -> None:
        ...

    @abstractmethod
    def assign_to(self, task_id: str, project_id: str) -> None:
        ...

    @abstractmethod
    def delegate_to(self, task_id: str, person: str) -> None:
        ...

    @abstractmethod
    def reclaim(self, task_id: str, state: str) -> None:
        ...

    @abstractmethod
    def schedule_on(self, task_id: str, date: datetime.date) -> None:
        ...

    @abstractmethod
    def update(self, id: str, title: str, description: str) -> None:
        ...


class Tasks(Projector):
    NAME = "tasks"
    TYPE = ProjectorTypes.RUN_FROM_BEGINNING

    def __init__(self, projection: TaskProjection) -> None:
        self.__projection = projection

    def when_task_captured(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.capture(
            data["task_id"], data["user_id"], data["title"], data["description"]
        )

    def when_task_eliminated(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.ELIMINATED.value)

    def when_task_filed(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.FILED.value)

    def when_task_incubated(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.INCUBATED.value)

    def when_task_done(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.DONE.value)

    def when_task_delegated_to(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.delegate_to(data["task_id"], data["person"])

    def when_task_reclaimed(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.reclaim(data["task_id"], TaskStates.ACTIONABLE.value)

    def when_task_assigned_to(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.assign_to(data["task_id"], data["project_id"])

    def when_task_scheduled(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.schedule_on(
            data["task_id"], datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
        )

    def when_task_actionable(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.ACTIONABLE.value)

    def when_task_updated(
        self, recorded_at: datetime.datetime, data: dict[str, str]
    ) -> None:
        self.__projection.update(data["task_id"], data["title"], data["description"])
