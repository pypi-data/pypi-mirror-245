# Gertrude --- GTD done right
# Copyright © 2022, 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from bl3d.event_sourcing import History

from . import events
from .entities import Task, User
from .value_objects import TaskId, UserId


class DomainHistory(History):
    EVENT_MODULE = events


class Tasks:
    def __init__(self, history: DomainHistory) -> None:
        self.__history = history

    def load(self, identifier: TaskId) -> Optional[Task]:
        if events := self.__history.read(str(identifier)):
            return Task.instanciate(events)  # type: ignore[arg-type]
        return None

    def next_id(self) -> TaskId:
        return TaskId.create()


class Users:
    def load(self, identifier: UserId) -> User:
        return User(identifier)

    def next_id(self) -> UserId:
        return UserId.create()
