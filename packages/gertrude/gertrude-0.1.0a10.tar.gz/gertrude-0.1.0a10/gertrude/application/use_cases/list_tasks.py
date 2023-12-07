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

from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.projections import Tasks


@dataclass(frozen=True)
class Request:
    user_id: str
    state: str = ""


class Presenter(ABC):
    @abstractmethod
    def unknown_state(self, name: str) -> None:
        pass

    @abstractmethod
    def tasks(self, some_tasks: list[Task]) -> None:
        pass


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    tasks: Tasks

    def execute(self, request: Request) -> None:
        if not request.state:
            self.presenter.tasks(self.tasks.all())
        else:
            try:
                state = TaskStates(request.state)
            except ValueError:
                return self.presenter.unknown_state(request.state)

            self.presenter.tasks(self.tasks.all(state=state.value))
