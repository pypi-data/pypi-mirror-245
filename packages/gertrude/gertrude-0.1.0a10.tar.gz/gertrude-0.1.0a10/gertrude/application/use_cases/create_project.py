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
from gertrude.domain.project_management.value_objects import Name, ProjectId, ShortName


@dataclass(frozen=True)
class Request:
    id: str
    name: str
    short_name: str


class Presenter(ABC):
    @abstractmethod
    def missing_id(self) -> None:
        ...

    @abstractmethod
    def missing_name(self) -> None:
        ...

    @abstractmethod
    def missing_short_name(self) -> None:
        ...

    @abstractmethod
    def project_already_exists(self) -> None:
        ...

    @abstractmethod
    def project_created(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    projects: Projects

    def execute(self, request: Request) -> None:
        if project := self.__instanciate_project(request):
            if not self.__exists(project):
                self.__save(project)

    def __instanciate_project(self, request: Request) -> Optional[Project]:
        project_id = self.__instanciate_project_id(request.id)
        name = self.__instanciate_name(request.name)
        short_name = self.__instanciate_short_name(request.short_name)

        if project_id and name and short_name:
            return Project(project_id, name, short_name)
        return None

    def __instanciate_project_id(self, value: str) -> Optional[ProjectId]:
        try:
            return ProjectId.instanciate(value)
        except Exception:
            return self.presenter.missing_id()

    def __instanciate_name(self, value: str) -> Optional[Name]:
        try:
            return Name.instanciate(value)
        except Exception:
            return self.presenter.missing_name()

    def __instanciate_short_name(self, value: str) -> Optional[ShortName]:
        try:
            return ShortName.instanciate(value)
        except Exception:
            return self.presenter.missing_short_name()

    def __exists(self, project: Project) -> bool:
        if self.projects.by_id(project.id):
            self.presenter.project_already_exists()
            return True
        return False

    def __save(self, project: Project) -> None:
        self.projects.save(project)
        self.presenter.project_created()
