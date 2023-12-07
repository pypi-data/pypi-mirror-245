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

from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.repositories import Projects
from gertrude.domain.project_management.value_objects import ProjectId
from gertrude.domain.task_management.entities import Task
from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.exceptions import TransitionNotAllowed
from gertrude.domain.task_management.repositories import DomainHistory, Tasks
from gertrude.domain.task_management.value_objects import ProjectId as TProjectId
from gertrude.domain.task_management.value_objects import TaskId


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str
    project_id: str


class Presenter(ABC):
    @abstractmethod
    def validation_error(self, attribute: str, exception: Exception) -> None:
        ...

    @abstractmethod
    def task_not_found(self) -> None:
        ...

    @abstractmethod
    def project_not_found(self) -> None:
        ...

    @abstractmethod
    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        ...

    @abstractmethod
    def task_assigned(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks
    projects: Projects

    def execute(self, request: Request) -> None:
        task = self.__find_task(request.task_id)
        project = self.__find_project(request.project_id)

        if task and project:
            self.__assign_to(task, project)

    def __find_task(self, id: str) -> Optional[Task]:
        try:
            task_id = TaskId.instanciate(id)
        except Exception as exc:
            return self.presenter.validation_error("task_id", exc)

        if task := self.tasks.load(task_id):
            return task
        else:
            return self.presenter.task_not_found()

    def __find_project(self, id: str) -> Optional[Project]:
        try:
            project_id = ProjectId.instanciate(id)
        except Exception as exc:
            return self.presenter.validation_error("project_id", exc)

        if project := self.projects.by_id(project_id):
            return project
        else:
            return self.presenter.project_not_found()

    def __assign_to(self, task: Task, project: Project) -> None:
        try:
            self.history << task.assign_to(TProjectId(str(project.id)))
        except TransitionNotAllowed as exc:
            return self.presenter.transition_not_allowed(exc.current, exc.next)
        return self.presenter.task_assigned()
