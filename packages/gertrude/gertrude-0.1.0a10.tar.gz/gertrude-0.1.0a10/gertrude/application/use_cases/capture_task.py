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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from gertrude.domain.task_management.entities import Task
from gertrude.domain.task_management.repositories import DomainHistory, Tasks, Users
from gertrude.domain.task_management.services import capture_task
from gertrude.domain.task_management.value_objects import (
    Description,
    ProjectId,
    TaskId,
    Title,
    UserId,
)


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str
    title: str
    description: str = ""
    project_id: str = ""


class Presenter(ABC):
    @abstractmethod
    def validation_error(self, attribute: str, exception: Exception) -> None:
        ...

    @abstractmethod
    def task_id_already_used(self) -> None:
        ...

    @abstractmethod
    def task_captured(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks
    users: Users

    def execute(self, request: Request) -> None:
        task: Optional[Task] = None

        task_id = self.__instanciate_task_id(request.task_id)
        user_id = self.__instanciate_user_id(request.user_id)
        title = self.__instanciate_title(request.title)
        description = self.__instanciate_description(request.description)
        project_id = self.__instanciate_project_id(request.project_id)

        if task_id and self.tasks.load(task_id):
            return self.presenter.task_id_already_used()

        if task_id and user_id and title and description:
            task = self.__capture(task_id, user_id, title, description)

        if task and project_id:
            self.__assign_to(task, project_id)

    def __capture(
        self, task_id: TaskId, user_id: UserId, title: Title, description: Description
    ) -> Optional[Task]:
        events = capture_task(task_id, user_id, title, description)
        self.history << events
        self.presenter.task_captured()
        return Task.instanciate(events)  # type: ignore

    def __assign_to(self, task: Task, project_id: ProjectId) -> None:
        self.history << task.assign_to(project_id)

    def __instanciate_task_id(self, value: str) -> Optional[TaskId]:
        try:
            return TaskId.instanciate(value)
        except Exception as exc:
            return self.presenter.validation_error("task_id", exc)

    def __instanciate_user_id(self, value: str) -> Optional[UserId]:
        try:
            return UserId.instanciate(value)
        except Exception as exc:
            return self.presenter.validation_error("user_id", exc)

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

    def __instanciate_project_id(self, value: str) -> Optional[ProjectId]:
        # Project ID is optional
        if not value:
            return None
        try:
            return ProjectId.instanciate(value)
        except Exception as exc:
            return self.presenter.validation_error("project_id", exc)
