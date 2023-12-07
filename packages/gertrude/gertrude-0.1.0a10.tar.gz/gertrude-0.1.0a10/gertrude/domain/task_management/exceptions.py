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

import datetime

from .enums import TaskStates


class MissingValue(Exception):
    pass


class TransitionNotAllowed(Exception):
    def __init__(self, current: TaskStates, next: TaskStates) -> None:
        self.current = current
        self.next = next


class DateInThePast(Exception):
    def __init__(self, current: datetime.date, target: datetime.date) -> None:
        self.current = current
        self.target = target
