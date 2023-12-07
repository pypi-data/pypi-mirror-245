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

from typing import Any, Optional

from gertrude.domain.project_management.entities import Project
from gertrude.domain.task_management.dto import Task
from gertrude.interfaces.to_http.as_html import OnSuccessTrigger, PugBody, Services
from gertrude.interfaces.to_http.presenters import (
    AssignTask,
    CaptureTask,
    DelegateTask,
    DoTask,
    EliminateTask,
    FileTask,
    IncubateTask,
    PostponeTask,
    ReclaimTask,
    ScheduleTask,
    UpdateTask,
)

MODAL_ID = "modal"


def capture_task(
    projects: list[Project], data: dict[str, Any], services: Services
) -> CaptureTask:
    return CaptureTask(
        OnSuccessTrigger(["TaskCaptured", "TasksChanged"]),
        PugBody(f"tasks/capture#{MODAL_ID}", services.create_context()),
        services.translate,
        data,
        projects,
    )


def do_task(task: Optional[Task], services: Services) -> DoTask:
    url = (
        services.url_for("projects.display", id=task.assigned_to)
        if task and task.assigned_to
        else ""
    )
    return DoTask(
        OnSuccessTrigger(["TaskDone", "TasksChanged"], url),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
    )


def incubate_task(task: Optional[Task], services: Services) -> IncubateTask:
    return IncubateTask(
        OnSuccessTrigger(["TaskIncubatene", "TasksChanged"]),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
    )


def file_task(task: Optional[Task], services: Services) -> FileTask:
    return FileTask(
        OnSuccessTrigger(["TaskFiled", "TasksChanged"]),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
    )


def postpone_task(task: Optional[Task], services: Services) -> PostponeTask:
    return PostponeTask(
        OnSuccessTrigger(["TaskPostponed", "TasksChanged"]),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
    )


def eliminate_task(task: Optional[Task], services: Services) -> EliminateTask:
    return EliminateTask(
        OnSuccessTrigger(["TaskEliminated", "TasksChanged"]),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
    )


def reclaim_task(task: Optional[Task], services: Services) -> ReclaimTask:
    return ReclaimTask(
        OnSuccessTrigger(["TaskReclaimed", "TasksChanged"]),
        PugBody(f"tasks/display#{MODAL_ID}", services.create_context()),
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
        OnSuccessTrigger(["TaskAssigned", "TasksChanged"]),
        PugBody(f"tasks/assign#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
        projects,
        data,
    )


def delegate_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> DelegateTask:
    return DelegateTask(
        OnSuccessTrigger(["TaskDelegated", "TasksChanged"]),
        PugBody(f"tasks/delegate#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
        data,
    )


def schedule_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> ScheduleTask:
    return ScheduleTask(
        OnSuccessTrigger(["TaskScheduled", "TasksChanged"]),
        PugBody(f"tasks/schedule#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
        data,
    )


def update_task(
    task: Optional[Task], data: dict[str, str], services: Services
) -> UpdateTask:
    return UpdateTask(
        OnSuccessTrigger(["TaskUpdated", "TasksChanged"]),
        PugBody(f"tasks/update#{MODAL_ID}", services.create_context()),
        services.translate,
        task,
        data,
    )
