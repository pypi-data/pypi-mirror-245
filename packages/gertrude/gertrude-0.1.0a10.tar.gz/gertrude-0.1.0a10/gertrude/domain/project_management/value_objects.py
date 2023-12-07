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

from typing import Type, TypeVar
from uuid import uuid4

from bl3d import String

A = TypeVar("A", bound="AggregateRootId")


class AggregateRootId(String):
    MIN: int = 36
    MAX: int = 36

    @classmethod
    def create(cls: Type[A]) -> A:
        return cls.instanciate(str(uuid4()))


class ProjectId(AggregateRootId):
    pass


class Name(String):
    MIN: int = 1
    MAX: int = 100


class ShortName(String):
    MIN: int = 1
    MAX: int = 10
