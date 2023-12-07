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

from http import HTTPStatus as HTTP
from typing import Optional

from gertrude.domain.project_management.entities import Project
from gertrude.domain.task_management.dto import Task
from gertrude.interfaces.to_http import Headers
from gertrude.interfaces.to_http.as_html import OnFailureRedirect, PugBody, Services
from gertrude.interfaces.to_http.presenters import (
    DisplayProject,
    DisplayTask,
    Inbox,
    Next,
    Organize,
    Scheduled,
    Someday,
    Waiting,
)

TASKS_ID = "tasks"
MODAL_ID = "modal"


def display_project(services: Services, fragment_only: bool) -> DisplayProject:
    fragment = TASKS_ID if fragment_only else ""
    return DisplayProject(
        OnFailureRedirect(services.url_for("projects.list")),
        PugBody(f"projects/display#{fragment}", services.create_context()),
        services.translate,
    )


def inbox(tasks: list[Task], services: Services, fragment_only: bool) -> Inbox:
    fragment = TASKS_ID if fragment_only else ""
    return Inbox(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/inbox#{fragment}", services.create_context()),
        tasks,
    )


def organize(
    tasks: list[Task], projects: list[Project], services: Services, fragment_only: bool
) -> Organize:
    fragment = TASKS_ID if fragment_only else ""
    return Organize(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/organize#{fragment}", services.create_context()),
        tasks,
        projects,
    )


def next(tasks: list[Task], services: Services, fragment_only: bool) -> Next:
    fragment = TASKS_ID if fragment_only else ""
    return Next(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/next#{fragment}", services.create_context()),
        tasks,
    )


def waiting(tasks: list[Task], services: Services, fragment_only: bool) -> Waiting:
    fragment = TASKS_ID if fragment_only else ""
    return Waiting(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/waiting#{fragment}", services.create_context()),
        tasks,
    )


def scheduled(tasks: list[Task], services: Services, fragment_only: bool) -> Scheduled:
    fragment = TASKS_ID if fragment_only else ""
    return Scheduled(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/scheduled#{fragment}", services.create_context()),
        tasks,
    )


def someday(tasks: list[Task], services: Services, fragment_only: bool) -> Someday:
    fragment = TASKS_ID if fragment_only else ""
    return Someday(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/someday#{fragment}", services.create_context()),
        tasks,
    )


def display_task(
    task: Optional[Task],
    projects: list[Project],
    services: Services,
    fragment_only: bool,
) -> DisplayTask:
    fragment = MODAL_ID if fragment_only else ""
    return DisplayTask(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody(f"tasks/display#{fragment}", services.create_context()),
        task,
        projects,
    )
