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
from typing import Any, Callable, Optional

from gertrude.domain.project_management.entities import Project
from gertrude.domain.task_management.dto import Task
from gertrude.interfaces.to_http import Headers
from gertrude.interfaces.to_http.as_html import OnSuccessRedirect, PugBody, Services
from gertrude.interfaces.to_http.presenters import (
    AssignTask,
    CaptureTask,
    CreateProject,
    DelegateTask,
    DoTask,
    EliminateTask,
    FileTask,
    IncubateTask,
    ListProjects,
    PostponeTask,
    ReclaimTask,
    ScheduleTask,
    UpdateTask,
)

Notifier = Callable[[str, str], None]


def list_projects(services: Services) -> ListProjects:
    return ListProjects(
        Headers(HTTP.OK, {"Content-Type": "text/html"}),
        PugBody("projects/list", services.create_context()),
    )


def create_project(data: dict[str, Any], services: Services) -> CreateProject:
    return CreateProject(
        OnSuccessRedirect(services.url_for("projects.list")),
        PugBody("projects/create", services.create_context()),
        services.translate,
        data,
    )


def capture_task(
    projects: list[Project], data: dict[str, Any], services: Services
) -> CaptureTask:
    return CaptureTask(
        OnSuccessRedirect(services.url_for("tasks.inbox")),
        PugBody("tasks/capture", services.create_context()),
        services.translate,
        data,
        projects,
    )


def do_task(task: Optional[Task], services: Services) -> DoTask:
    url = (
        services.url_for("projects.display", id=task.assigned_to)
        if task and task.assigned_to
        else services.url_for("tasks.inbox")
    )
    return DoTask(
        OnSuccessRedirect(url, services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def incubate_task(task: Optional[Task], services: Services) -> IncubateTask:
    return IncubateTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def file_task(task: Optional[Task], services: Services) -> FileTask:
    return FileTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def postpone_task(task: Optional[Task], services: Services) -> PostponeTask:
    return PostponeTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def eliminate_task(task: Optional[Task], services: Services) -> EliminateTask:
    return EliminateTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def reclaim_task(task: Optional[Task], services: Services) -> ReclaimTask:
    return ReclaimTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/display", services.create_context()),
        services.translate,
        task,
    )


def assign_task(
    task: Optional[Task],
    projects: list[Project],
    data: dict[str, str],
    services: Services,
) -> AssignTask:
    return AssignTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/assign", services.create_context()),
        services.translate,
        task,
        projects,
        data,
    )


def delegate_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> DelegateTask:
    return DelegateTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/delegate", services.create_context()),
        services.translate,
        task,
        data,
    )


def schedule_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> ScheduleTask:
    return ScheduleTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/schedule", services.create_context()),
        services.translate,
        task,
        data,
    )


def update_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> UpdateTask:
    return UpdateTask(
        OnSuccessRedirect(services.url_for("tasks.inbox"), services.notify),
        PugBody("tasks/update", services.create_context()),
        services.translate,
        task,
        data,
    )
