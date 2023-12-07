# Gertrude --- GTD done right
# Copyright © 2021, 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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
from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.projections import Tasks


@dataclass(frozen=True)
class Request:
    id: str


class Presenter(ABC):
    @abstractmethod
    def project_not_found(self, id: str) -> None:
        ...

    @abstractmethod
    def project(self, project: Project) -> None:
        ...

    @abstractmethod
    def task(self, task: Task) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    projects: Projects
    tasks: Tasks

    def execute(self, request: Request) -> None:
        if project := self.__load_project(request.id):
            self.__load_related_tasks(project)

    def __load_project(self, id: str) -> Optional[Project]:
        try:
            project_id = ProjectId.instanciate(id)
        except Exception:
            return self.presenter.project_not_found(id)

        if project := self.projects.by_id(project_id):
            self.presenter.project(project)
            return project
        return self.presenter.project_not_found(id)

    def __load_related_tasks(self, project: Project) -> None:
        for task in self.tasks.all(assigned_to=str(project.id)):
            self.presenter.task(task)
