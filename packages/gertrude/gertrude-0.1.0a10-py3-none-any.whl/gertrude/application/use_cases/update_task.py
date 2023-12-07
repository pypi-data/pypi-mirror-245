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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from gertrude.domain.task_management.entities import Task
from gertrude.domain.task_management.repositories import DomainHistory, Tasks
from gertrude.domain.task_management.value_objects import Description, TaskId, Title


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str
    title: str
    description: str = ""


class Presenter(ABC):
    @abstractmethod
    def validation_error(self, attribute: str, exception: Exception) -> None:
        ...

    @abstractmethod
    def task_not_found(self) -> None:
        ...

    @abstractmethod
    def task_updated(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks

    def execute(self, request: Request) -> None:
        if task := self.__find_task(request.task_id):
            self.__update(task, request)

    def __find_task(self, task_id: str) -> Optional[Task]:
        try:
            id = TaskId.instanciate(task_id)
        except Exception as exc:
            return self.presenter.validation_error("task_id", exc)

        if task := self.tasks.load(id):
            return task
        return self.presenter.task_not_found()

    def __update(self, task: Task, request: Request) -> None:
        title = self.__instanciate_title(request.title)
        description = self.__instanciate_description(request.description)

        if title and description:
            self.history << task.update(title, description)
            self.presenter.task_updated()

    def __instanciate_title(self, value: str) -> Optional[Title]:
        try:
            return Title.instanciate(value)
        except Exception as exc:
            return self.presenter.validation_error("title", exc)

    def __instanciate_description(self, value: str) -> Optional[Description]:
        try:
            return Description.instanciate(value)
        except Exception as exc:
            return self.presenter.validation_error("description", exc)
