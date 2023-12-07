# Gertrude --- GTD done right
# Copyright © 2020, 2021, 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from gertrude.domain.task_management.entities import Task
from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.exceptions import TransitionNotAllowed
from gertrude.domain.task_management.repositories import DomainHistory, Tasks
from gertrude.domain.task_management.value_objects import TaskId


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str


class Presenter(ABC):
    @abstractmethod
    def validation_error(self, attribute: str, exception: Exception) -> None:
        ...

    @abstractmethod
    def task_not_found(self) -> None:
        ...

    @abstractmethod
    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        ...

    @abstractmethod
    def task_postponed(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks

    def execute(self, request: Request) -> None:
        if task := self.__find_task(request.task_id):
            self.__postpone(task)

    def __find_task(self, task_id: str) -> Optional[Task]:
        try:
            id = TaskId.instanciate(task_id)
        except Exception as exc:
            return self.presenter.validation_error("task_id", exc)

        if task := self.tasks.load(id):
            return task
        return self.presenter.task_not_found()

    def __postpone(self, task: Task) -> None:
        try:
            self.history << task.mark_as_actionable()
        except TransitionNotAllowed as exc:
            return self.presenter.transition_not_allowed(exc.current, exc.next)
        return self.presenter.task_postponed()
