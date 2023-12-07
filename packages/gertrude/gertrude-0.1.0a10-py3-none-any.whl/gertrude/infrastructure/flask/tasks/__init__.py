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

from typing import Any

from flask import Blueprint, request

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    delegate_task,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    postpone_task,
    reclaim_task,
    schedule_task,
    update_task,
)
from gertrude.infrastructure.flask import presenters, services
from gertrude.infrastructure.flask.utils import (
    auth_required,
    htmx,
    presenter_to_response,
)
from gertrude.interfaces import from_base_types as controllers
from gertrude.interfaces.to_http import as_html

blueprint = Blueprint("tasks", __name__)


@blueprint.get("")
@presenter_to_response
def index() -> Any:
    return as_html.HtmlPresenter.from_template(
        "tasks/index", **presenters.Services().create_context()
    )


@blueprint.get("/__new__")
@presenter_to_response
@auth_required
def capture_form() -> Any:
    return presenters.capture_task({}, bool(htmx))


@blueprint.post("/__new__")
@presenter_to_response
@auth_required
def capture() -> Any:
    presenter = presenters.capture_task(request.form, bool(htmx))
    interactor = capture_task.Interactor(
        presenter, services.history(), services.tasks(), services.users()
    )
    controller = controllers.CaptureTask(services.user_id(), request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/inbox")
@presenter_to_response
@auth_required
def inbox() -> Any:
    return presenters.inbox(bool(htmx))


@blueprint.get("/organize")
@presenter_to_response
@auth_required
def organize() -> Any:
    return presenters.organize(bool(htmx))


@blueprint.get("/next")
@presenter_to_response
@auth_required
def next() -> Any:
    return presenters.next(bool(htmx))


@blueprint.get("/waiting")
@presenter_to_response
@auth_required
def waiting() -> Any:
    return presenters.waiting(bool(htmx))


@blueprint.get("/scheduled")
@presenter_to_response
@auth_required
def scheduled() -> Any:
    return presenters.scheduled(bool(htmx))


@blueprint.get("/someday")
@presenter_to_response
@auth_required
def someday() -> Any:
    return presenters.someday(bool(htmx))


@blueprint.get("/<id>")
@presenter_to_response
@auth_required
def display(id: str) -> Any:
    return presenters.display_task(id, bool(htmx))


@blueprint.post("/<id>/__do__")
@presenter_to_response
@auth_required
def do(id: str) -> Any:
    presenter = presenters.do_task(id, bool(htmx))
    interactor = do_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.DoTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.post("/<id>/__incubate__")
@presenter_to_response
@auth_required
def incubate(id: str) -> Any:
    presenter = presenters.incubate_task(id, bool(htmx))
    interactor = incubate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.IncubateTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.post("/<id>/__file__")
@presenter_to_response
@auth_required
def file(id: str) -> Any:
    presenter = presenters.file_task(id, bool(htmx))
    interactor = file_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.FileTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.post("/<id>/__postpone__")
@presenter_to_response
@auth_required
def postpone(id: str) -> Any:
    presenter = presenters.postpone_task(id, bool(htmx))
    interactor = postpone_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.PostponeTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.post("/<id>/__eliminate__")
@presenter_to_response
@auth_required
def eliminate(id: str) -> Any:
    presenter = presenters.eliminate_task(id, bool(htmx))
    interactor = eliminate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.EliminateTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.post("/<id>/__reclaim__")
@presenter_to_response
@auth_required
def reclaim(id: str) -> Any:
    presenter = presenters.reclaim_task(id, bool(htmx))
    interactor = reclaim_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.ReclaimTask(services.user_id(), id)
    controller.call(interactor)
    return presenter


@blueprint.get("/<id>/__assign__")
@presenter_to_response
@auth_required
def assign_form(id: str) -> Any:
    return presenters.assign_task(id, {}, bool(htmx))


@blueprint.post("/<id>/__assign__")
@presenter_to_response
@auth_required
def assign(id: str) -> Any:
    presenter = presenters.assign_task(id, request.form, bool(htmx))
    interactor = assign_task.Interactor(
        presenter, services.history(), services.tasks(), services.projects()
    )
    controller = controllers.AssignTask(services.user_id(), id, request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/<id>/__delegate__")
@presenter_to_response
@auth_required
def delegate_form(id: str) -> Any:
    return presenters.delegate_task(id, request.form, bool(htmx))


@blueprint.post("/<id>/__delegate__")
@presenter_to_response
@auth_required
def delegate(id: str) -> Any:
    presenter = presenters.delegate_task(id, request.form, bool(htmx))
    interactor = delegate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.DelegateTask(services.user_id(), id, request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/<id>/__schedule__")
@presenter_to_response
@auth_required
def schedule_form(id: str) -> Any:
    return presenters.schedule_task(id, request.form, bool(htmx))


@blueprint.post("/<id>/__schedule__")
@presenter_to_response
@auth_required
def schedule(id: str) -> Any:
    presenter = presenters.schedule_task(id, request.form, bool(htmx))
    interactor = schedule_task.Interactor(
        presenter, services.history(), services.tasks(), services.calendar()
    )
    controller = controllers.ScheduleTask(services.user_id(), id, request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/<id>/__update__")
@presenter_to_response
@auth_required
def update_form(id: str) -> Any:
    return presenters.update_task(id, request.form, bool(htmx))


@blueprint.post("/<id>/__update__")
@presenter_to_response
@auth_required
def update(id: str) -> Any:
    presenter = presenters.update_task(id, request.form, bool(htmx))
    interactor = update_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.UpdateTask(services.user_id(), id, request.form)
    controller.call(interactor)
    return presenter
