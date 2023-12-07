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

from dataclasses import dataclass
from typing import Optional

from bl3d.event_sourcing import DomainEvent


@dataclass(frozen=True)
class TaskEvent(DomainEvent):
    task_id: str

    @property
    def aggregate_id(self) -> str:
        return self.task_id


@dataclass(frozen=True)
class TaskCaptured(TaskEvent):
    user_id: str
    title: str
    description: Optional[str] = ""


@dataclass(frozen=True)
class TaskEliminated(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskFiled(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskIncubated(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskDone(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskDelegatedTo(TaskEvent):
    person: str


@dataclass(frozen=True)
class TaskReclaimed(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskScheduled(TaskEvent):
    date: str


@dataclass(frozen=True)
class TaskActionable(TaskEvent):
    pass


@dataclass(frozen=True)
class TaskAssignedTo(TaskEvent):
    project_id: str


@dataclass(frozen=True)
class TaskUpdated(TaskEvent):
    title: str
    description: str
