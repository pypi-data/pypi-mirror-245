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

import datetime
from importlib.metadata import version
from typing import Any, Optional

from flask import get_flashed_messages, request, session, url_for

from gertrude import __name__ as PACKAGE_NAME
from gertrude.application import use_cases as uc
from gertrude.domain.project_management.entities import Project
from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.enums import TaskStates
from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import notify
from gertrude.interfaces import l10n
from gertrude.interfaces.to_http import IsPresentable
from gertrude.interfaces.to_http.as_html import Services as ServicesABC
from gertrude.interfaces.to_http.as_html import fragment, page, page_or_fragment


class Services(ServicesABC):
    def url_for(self, endpoint: str, **kwargs: Any) -> str:
        return url_for(endpoint, **kwargs)

    def notify(self, message: str, category: str) -> None:
        notify(message, category)

    def create_context(self) -> dict[str, Any]:
        locale = request.accept_languages.best_match(l10n.LOCALES) or l10n.DEFAULT_LOCALE
        return {
            "version": version(PACKAGE_NAME),
            "current_url": request.path,
            "url_for": url_for,
            "get_flashed_messages": get_flashed_messages,
            "_": l10n.translator_for(locale),
            "is_logged_in": "user_id" in session,
            "today": datetime.date.today(),
            "now": datetime.datetime.now(datetime.timezone.utc),
        }

    def translate(self, message: str, **kwargs: Any) -> str:
        _ = l10n.translator_for(
            request.accept_languages.best_match(l10n.LOCALES) or l10n.DEFAULT_LOCALE
        )
        return str(_(message, **kwargs))


def load_task(id: str) -> Optional[Task]:
    return services.task_projection().load(id)


def load_projects() -> list[Project]:
    return services.projects().all()


def list_projects() -> uc.list_projects.Presenter:
    return page.list_projects(Services())


def create_project(data: dict[str, Any]) -> uc.create_project.Presenter:
    return page.create_project(data, Services())


def display_project(fragment_only: bool) -> uc.display_project.Presenter:
    return page_or_fragment.display_project(Services(), fragment_only)


def inbox(fragment_only: bool) -> IsPresentable:
    return page_or_fragment.inbox(
        services.task_projection().all(state=TaskStates.CAPTURED.value),
        Services(),
        fragment_only,
    )


def organize(fragment_only: bool) -> IsPresentable:
    return page_or_fragment.organize(
        services.task_projection().all(), load_projects(), Services(), fragment_only
    )


def next(fragment_only: bool) -> IsPresentable:
    tasks = services.task_projection()
    return page_or_fragment.next(
        tasks.all(state=TaskStates.ACTIONABLE.value) + tasks.due(datetime.date.today()),
        Services(),
        fragment_only,
    )


def waiting(fragment_only: bool) -> IsPresentable:
    return page_or_fragment.waiting(
        services.task_projection().all(state=TaskStates.DELEGATED.value),
        Services(),
        fragment_only,
    )


def scheduled(fragment_only: bool) -> IsPresentable:
    return page_or_fragment.scheduled(
        services.task_projection().all(state=TaskStates.SCHEDULED.value),
        Services(),
        fragment_only,
    )


def someday(fragment_only: bool) -> IsPresentable:
    return page_or_fragment.someday(
        services.task_projection().all(state=TaskStates.INCUBATED.value),
        Services(),
        fragment_only,
    )


def capture_task(data: dict[str, Any], is_htmx: bool) -> uc.capture_task.Presenter:
    if not is_htmx:
        return page.capture_task(load_projects(), data, Services())
    return fragment.capture_task(load_projects(), data, Services())


def display_task(task_id: str, fragment_only: bool) -> IsPresentable:
    return page_or_fragment.display_task(
        load_task(task_id), load_projects(), Services(), fragment_only
    )


def do_task(task_id: str, fragment_only: bool) -> uc.do_task.Presenter:
    if not fragment_only:
        return page.do_task(load_task(task_id), Services())
    return fragment.do_task(load_task(task_id), Services())


def incubate_task(task_id: str, fragment_only: bool) -> uc.incubate_task.Presenter:
    if not fragment_only:
        return page.incubate_task(load_task(task_id), Services())
    return fragment.incubate_task(load_task(task_id), Services())


def file_task(task_id: str, fragment_only: bool) -> uc.file_task.Presenter:
    if not fragment_only:
        return page.file_task(load_task(task_id), Services())
    return fragment.file_task(load_task(task_id), Services())


def postpone_task(task_id: str, fragment_only: bool) -> uc.postpone_task.Presenter:
    if not fragment_only:
        return page.postpone_task(load_task(task_id), Services())
    return fragment.postpone_task(load_task(task_id), Services())


def eliminate_task(task_id: str, fragment_only: bool) -> uc.eliminate_task.Presenter:
    if not fragment_only:
        return page.eliminate_task(load_task(task_id), Services())
    return fragment.eliminate_task(load_task(task_id), Services())


def reclaim_task(task_id: str, fragment_only: bool) -> uc.reclaim_task.Presenter:
    if not fragment_only:
        return page.reclaim_task(load_task(task_id), Services())
    return fragment.reclaim_task(load_task(task_id), Services())


def assign_task(
    task_id: str, data: dict[str, Any], fragment_only: bool
) -> uc.assign_task.Presenter:
    if not fragment_only:
        return page.assign_task(load_task(task_id), load_projects(), data, Services())
    return fragment.assign_task(load_task(task_id), load_projects(), data, Services())


def delegate_task(
    task_id: str, data: dict[str, Any], fragment_only: bool
) -> uc.delegate_task.Presenter:
    if not fragment_only:
        return page.delegate_task(load_task(task_id), data, Services())
    return fragment.delegate_task(load_task(task_id), data, Services())


def schedule_task(
    task_id: str, data: dict[str, Any], fragment_only: bool
) -> uc.schedule_task.Presenter:
    if not fragment_only:
        return page.schedule_task(load_task(task_id), data, Services())
    return fragment.schedule_task(load_task(task_id), data, Services())


def update_task(
    task_id: str, data: dict[str, Any], fragment_only: bool
) -> uc.update_task.Presenter:
    if not fragment_only:
        return page.update_task(load_task(task_id), data, Services())
    return fragment.update_task(load_task(task_id), data, Services())
