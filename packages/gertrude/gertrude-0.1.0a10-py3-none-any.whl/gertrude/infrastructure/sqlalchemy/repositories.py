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

from typing import Optional

from sqlalchemy import Column, String, Table
from sqlalchemy.orm import Session, composite, registry

from gertrude.domain.project_management import value_objects as vo
from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.repositories import Projects as ProjectsABC

vo.String.__composite_values__ = lambda self: (str(self),)  # type: ignore[attr-defined]

REGISTRY = registry()
projects_table = Table(
    "projects",
    REGISTRY.metadata,
    Column("_id", String(vo.ProjectId.MAX), primary_key=True),
    Column("_name", String(vo.Name.MAX)),
    Column("_short_name", String(vo.ShortName.MAX)),
)
REGISTRY.map_imperatively(
    Project,
    projects_table,
    properties={
        "id": composite(vo.ProjectId, projects_table.c._id),
        "name": composite(vo.Name, projects_table.c._name),
        "short_name": composite(vo.ShortName, projects_table.c._short_name),
    },
)


class Projects(ProjectsABC):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def save(self, project: Project) -> None:
        self.__session.add(project)

    def by_id(self, id: vo.ProjectId) -> Optional[Project]:
        return self.__session.query(Project).get(id)

    def all(self) -> list[Project]:
        return self.__session.query(Project).all()
