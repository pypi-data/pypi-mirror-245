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

import datetime
from typing import Any, Optional

from sqlalchemy import Column, Date, MetaData, String, Table, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Executable

from gertrude.application import projectors
from gertrude.domain.task_management import dto, enums, projections, value_objects

METADATA = MetaData()
tasks_table = Table(
    "tasks",
    METADATA,
    Column("id", String),
    Column("title", String(value_objects.Title.MAX)),
    Column("description", String(value_objects.Description.MAX)),
    Column("state", String),
    Column("belongs_to", String(value_objects.UserId.MAX)),
    Column("assigned_to", String(value_objects.ProjectId.MAX), default=""),
    Column("delegated_to", String(value_objects.Person.MAX), default=""),
    Column("scheduled_on", Date, default=None),
)


class Tasks(projectors.TaskProjection, projections.Tasks):
    def __init__(self, session: Session, autocommit: bool = True) -> None:
        self.__session = session
        self.__autocommit = autocommit

    def __execute(self, statement: Executable) -> None:
        self.__session.execute(statement)
        if self.__autocommit:
            self.__session.commit()

    def capture(self, id: str, belongs_to: str, title: str, description: str) -> None:
        self.__execute(
            insert(tasks_table).values(
                id=id,
                title=title,
                description=description,
                state=enums.TaskStates.CAPTURED.value,
                belongs_to=belongs_to,
            )
        )

    def update_state(self, id: str, state: str) -> None:
        self.__execute(
            update(tasks_table).where(tasks_table.c.id == id).values(state=state)
        )

    def assign_to(self, id: str, assigned_to: str) -> None:
        self.__execute(
            update(tasks_table)
            .where(tasks_table.c.id == id)
            .values(assigned_to=assigned_to)
        )

    def delegate_to(self, id: str, delegated_to: str) -> None:
        self.__execute(
            update(tasks_table)
            .where(tasks_table.c.id == id)
            .values(state=enums.TaskStates.DELEGATED.value, delegated_to=delegated_to)
        )

    def reclaim(self, id: str, state: str) -> None:
        self.__execute(
            update(tasks_table)
            .where(tasks_table.c.id == id)
            .values(state=state, delegated_to="")
        )

    def schedule_on(self, id: str, date: datetime.date) -> None:
        self.__execute(
            update(tasks_table)
            .where(tasks_table.c.id == id)
            .values(state=enums.TaskStates.SCHEDULED.value, scheduled_on=date)
        )

    def update(self, id: str, title: str, description: str) -> None:
        self.__execute(
            update(tasks_table)
            .where(tasks_table.c.id == id)
            .values(title=title, description=description)
        )

    def load(self, id: str) -> Optional[dto.Task]:
        stmt = select(tasks_table).where(tasks_table.c.id == id)
        if row := self.__session.execute(stmt).fetchone():
            return self.__row_to_task(row)
        return None

    def all(self, /, *, state: str = "", assigned_to: str = "") -> list[dto.Task]:
        stmt = select(tasks_table)
        if state:
            stmt = stmt.where(tasks_table.c.state == state)
        if assigned_to:
            stmt = stmt.where(tasks_table.c.assigned_to == assigned_to)

        return [self.__row_to_task(r) for r in self.__session.execute(stmt).fetchall()]

    def __row_to_task(self, row: Row[Any]) -> dto.Task:
        return dto.Task(
            id=row.id,
            title=row.title,
            description=row.description,
            state=row.state,
            delegated_to=row.delegated_to,
            assigned_to=row.assigned_to,
            scheduled_on=row.scheduled_on,
        )

    def due(self, date: datetime.date) -> list[dto.Task]:
        stmt = (
            select(tasks_table)
            .where(tasks_table.c.state == enums.TaskStates.SCHEDULED.value)
            .where(tasks_table.c.scheduled_on <= date)
        )
        return [self.__row_to_task(r) for r in self.__session.execute(stmt).fetchall()]
