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

from typing import Any

from flask import Blueprint, request

from gertrude.application.use_cases import (
    create_project,
    display_project,
    list_projects,
)
from gertrude.infrastructure.flask import presenters, services
from gertrude.infrastructure.flask.utils import (
    auth_required,
    htmx,
    presenter_to_response,
)
from gertrude.interfaces import from_base_types as controllers

blueprint = Blueprint("projects", __name__)


@blueprint.get("")
@presenter_to_response
@auth_required
def list() -> Any:
    presenter = presenters.list_projects()
    interactor = list_projects.Interactor(presenter, services.projects())
    interactor.execute()
    return presenter


@blueprint.get("/__new__")
@presenter_to_response
@auth_required
def create() -> Any:
    return presenters.create_project({})


@blueprint.post("/__new__")
@presenter_to_response
@auth_required
def create_POST() -> Any:
    presenter = presenters.create_project(request.form.to_dict())
    interactor = create_project.Interactor(presenter, services.projects())
    controller = controllers.CreateProject(request.form.to_dict())
    controller.call(interactor)
    return presenter


@blueprint.get("/<id>")
@presenter_to_response
@auth_required
def display(id: str) -> Any:
    presenter = presenters.display_project(bool(htmx))
    interactor = display_project.Interactor(
        presenter, services.projects(), services.task_projection()
    )
    controller = controllers.DisplayProject(id)
    controller.call(interactor)
    return presenter
