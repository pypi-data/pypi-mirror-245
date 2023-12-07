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
import logging
from dataclasses import asdict
from http import HTTPStatus as HTTP
from typing import Any, Optional, Protocol

import bl3d
import markdown

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    create_project,
    delegate_task,
    display_project,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    list_projects,
    postpone_task,
    reclaim_task,
    schedule_task,
    update_task,
)
from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.value_objects import Name, ProjectId, ShortName
from gertrude.domain.task_management import exceptions
from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.entities import POSSIBLE_NEXT_STATES_OF_TASK
from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.value_objects import (
    Description,
    Person,
    TaskId,
    Title,
)

from . import EmptyBody, Headers, IsPresentable, MessageBody


class Translator(Protocol):
    def __call__(self, message: str, **kwargs: Any) -> str:
        ...


class ListProjects(list_projects.Presenter, IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody) -> None:
        self.headers = headers
        self.body = body
        self.body["projects"] = []

    def projects(self, projects: list[Project]) -> None:
        self.body["projects"] = projects


class CreateProject(create_project.Presenter, IsPresentable):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        data: dict[str, Any],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["values"] = data or {"id": str(ProjectId.create())}
        self.body["errors"] = {}
        self.body["short_name_max"] = ShortName.MAX
        self.body["name_max"] = Name.MAX
        self._ = translator

    def missing_id(self) -> None:
        self.headers.status_code = HTTP.BAD_REQUEST
        self.body["errors"]["name"] = self._("pages-projects-create-missing-id")

    def missing_name(self) -> None:
        self.body["errors"]["name"] = self._("pages-projects-create-missing-name")

    def missing_short_name(self) -> None:
        self.body["errors"]["short_name"] = self._(
            "pages-projects-create-missing-short-name"
        )

    def project_already_exists(self) -> None:
        self.body["errors"]["name"] = self._(
            "pages-projects-create-project-already-exists"
        )

    def project_created(self) -> None:
        self.headers.success(self._("pages-projects-create-project-created"))


class DisplayProject(display_project.Presenter, IsPresentable):
    def __init__(
        self, headers: Headers, body: MessageBody, translator: Translator
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["project"] = {}
        self.body["tasks"] = []
        self.body["actionable_tasks"] = []
        self.body["incubated_tasks"] = []
        self.body["done_tasks"] = []
        self._ = translator

    def project_not_found(self, id: str) -> None:
        self.headers.failure(self._("pages-projects-display-project-not-found"))
        self.body = EmptyBody()

    def project(self, project: Project) -> None:
        self.body["project"] = project

    def task(self, task: Task) -> None:
        if task.state == TaskStates.ACTIONABLE.value:
            self.body["tasks"].append(task)
            self.body["actionable_tasks"].append(task)
        elif task.state == TaskStates.INCUBATED.value:
            self.body["tasks"].append(task)
            self.body["incubated_tasks"].append(task)
        elif task.state == TaskStates.DONE.value:
            self.body["done_tasks"].append(task)


class Inbox(IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody, tasks: list[Task]) -> None:
        self.headers = headers
        self.body = body
        self.body["tasks"] = tasks


class Organize(IsPresentable):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        tasks: list[Task],
        projects: list[Project],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["tasks"] = tasks
        self.body["projects_by_id"] = {p.id: p for p in projects}


class Next(IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody, tasks: list[Task]) -> None:
        self.headers = headers
        self.body = body
        self.body["tasks"] = tasks


class Waiting(IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody, tasks: list[Task]) -> None:
        self.headers = headers
        self.body = body
        self.body["persons_and_tasks"] = self.__persons_and_tasks(tasks)

    def __persons_and_tasks(self, tasks: list[Task]) -> list[tuple[str, list[Task]]]:
        resultat = []
        for person in set([t.delegated_to for t in tasks]):
            resultat.append((person, [t for t in tasks if t.delegated_to == person]))
        return sorted(resultat, key=lambda r: r[0])


class Scheduled(IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody, tasks: list[Task]) -> None:
        self.headers = headers
        self.body = body
        self.body["tasks"] = sorted(tasks, key=lambda t: t.scheduled_on)


class Someday(IsPresentable):
    def __init__(self, headers: Headers, body: MessageBody, tasks: list[Task]) -> None:
        self.headers = headers
        self.body = body
        self.body["tasks"] = tasks


class CaptureTask(IsPresentable, capture_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        data: dict[str, str],
        projects: list[Project],
    ) -> None:
        data = {**data} or {}
        data["task_id"] = data.get("task_id", str(TaskId.create()))
        body["values"] = data
        body["errors"] = {}
        body["max"] = {"title": Title.MAX, "description": Description.MAX}
        body["projects"] = sorted(projects, key=lambda p: str(p.name))
        self.headers = headers
        self.body = body
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_id_already_used(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-capture-task-id-already-used")

    def task_captured(self) -> None:
        self.headers.success(self._("pages-tasks-capture-taks-captured"))
        self.body = EmptyBody()


class DisplayTask(IsPresentable):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        task: Optional[Task],
        projects: list[Project],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["projects_by_id"] = {str(p.id): p for p in projects}
        self.body["possible_next_states"] = self.__possible_next_states(task)
        self.body["errors"] = {}

    def __possible_next_states(self, task: Optional[Task]) -> list[str]:
        if task and (current_state := TaskStates(task.state)):
            return [s.name for s in POSSIBLE_NEXT_STATES_OF_TASK[current_state]]
        return []


class DoTask(IsPresentable, do_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_done(self) -> None:
        self.headers.success(self._("pages-tasks-do-success"))
        self.body = EmptyBody()


class IncubateTask(IsPresentable, incubate_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_incubated(self) -> None:
        self.headers.success(self._("pages-tasks-incubate-success"))
        self.body = EmptyBody()


class FileTask(IsPresentable, file_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = "pages-tasks-errors-transition-not-allowed"

    def task_filed(self) -> None:
        self.headers.success(self._("pages-tasks-postpone-success"))
        self.body = EmptyBody()


class PostponeTask(IsPresentable, postpone_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_postponed(self) -> None:
        self.headers.success(self._("pages-tasks-postpone-success"))
        self.body = EmptyBody()


class EliminateTask(IsPresentable, eliminate_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_eliminated(self) -> None:
        self.headers.success(self._("pages-tasks-eliminate-success"))
        self.body = EmptyBody()


class ReclaimTask(IsPresentable, reclaim_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_reclaimed(self) -> None:
        self.headers.success(self._("pages-tasks-reclaim-success"))
        self.body = EmptyBody()


class AssignTask(IsPresentable, assign_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
        projects: list[Project],
        data: dict[str, str],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["projects"] = sorted(projects, key=lambda p: str(p.name))
        self.body["values"] = data
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def missing_project_id(self) -> None:
        self.body["errors"]["project_id"] = self._(
            "pages-tasks-assign-missing-project-id"
        )

    def incorrect_project_id(self) -> None:
        self.body["errors"]["project_id"] = self._(
            "pages-tasks-assign-incorrect-project-id"
        )

    def project_not_found(self) -> None:
        self.body["errors"]["project_id"] = self._(
            "pages-tasks-assign-project-not-found"
        )

    def task_assigned(self) -> None:
        self.headers.success(self._("pages-tasks-assign-success"))
        self.body = EmptyBody()


class DelegateTask(IsPresentable, delegate_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
        data: dict[str, str],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["values"] = data
        self.body["max"] = {"person": Person.MAX}
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_delegated(self) -> None:
        self.headers.success(self._("pages-tasks-delegate-success"))
        self.body = EmptyBody()


class ScheduleTask(IsPresentable, schedule_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
        data: dict[str, str],
    ) -> None:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        min_date = tomorrow.strftime("%Y-%m-%d")
        data = {**(data or {})}
        data["date"] = data.get("date", min_date)

        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["values"] = data
        self.body["min_date"] = min_date
        self.body["errors"] = {}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        self.body["errors"]["other"] = self._(
            "pages-tasks-errors-transition-not-allowed"
        )

    def task_scheduled(self) -> None:
        self.headers.success(self._("pages-tasks-schedule-success"))
        self.body = EmptyBody()


class UpdateTask(IsPresentable, update_task.Presenter):
    def __init__(
        self,
        headers: Headers,
        body: MessageBody,
        translator: Translator,
        task: Optional[Task],
        data: dict[str, str],
    ) -> None:
        self.headers = headers
        self.body = body
        self.body["task"] = format_task(task) if task else {}
        self.body["values"] = data or task
        self.body["errors"] = {}
        body["max"] = {"title": Title.MAX, "description": Description.MAX}
        self._ = translator

    def validation_error(self, attribute: str, exception: Exception) -> None:
        self.body["errors"][attribute] = translate_exception(exception, self._)

    def task_not_found(self) -> None:
        self.body["errors"]["other"] = self._("pages-tasks-errors-task-not-found")

    def task_updated(self) -> None:
        self.headers.success(self._("pages-tasks-update-success"))
        self.body = EmptyBody()


def format_task(task: Task) -> dict[str, Any]:
    data = asdict(task)
    data["description"] = markdown.markdown(task.description or "")
    return data


def translate_exception(exception: Exception, translator: Translator) -> str:
    if isinstance(exception, exceptions.MissingValue):
        return translator("exceptions-missing-value")
    if isinstance(exception, exceptions.TransitionNotAllowed):
        return translator(
            "exceptions-transition-not-allowed",
            current=exception.current.value,
            next=exception.next.value,
        )
    if isinstance(exception, exceptions.DateInThePast):
        return translator(
            "exceptions-date-in-the-past",
            current=exception.current,
            target=exception.target,
        )
    if isinstance(exception, bl3d.StringTooShort):
        return translator("exceptions-string-too-short", min=exception.MIN)
    if isinstance(exception, bl3d.StringTooLong):
        return translator("exceptions-string-too-long", max=exception.MAX)

    logging.debug(f"Unhandled exception cannot be translated! [{type(exception)}]")
    return translator("exceptions-unknown-exception", name=exception.__class__.__name__)
