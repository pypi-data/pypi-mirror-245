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

-project-name = Gertrude

activities-capture = Capture
activities-clarify = Clarify
activities-organize = Organize
activities-reflect = Reflect
activities-engage = Engage

categories-inbox = Inbox
categories-organize = Organize
categories-next = Next
categories-projects = Projects
categories-waiting = Waiting
categories-scheduled = Scheduled
categories-someday = Someday

exceptions-unknown-exception = An unknown error occurred! [`{ $name }`]
exceptions-missing-value = This value is mandatory!
exceptions-transition-not-allowed = This transition is impossible
exceptions-date-in-the-past = The date cannot be in the past!
exceptions-string-too-long =
    { $max ->
        [one] This value must be at most one character long!
       *[other] This value must be at most { $max } character(s) long!
    }
exceptions-string-too-short =
    { $min ->
        [one] This value must be at least one character long!
       *[other] This value must be at least { $min } character(s) long!
    }

pages-auth-login-title = Log into { -project-name }
pages-auth-login-link = Log in with { $label }

pages-error-title = An error has occurred!

pages-layout-title = { -project-name }
pages-layout-footer-html =
    <p>
        Version { $version } © { $years } Bioneland.
        <br />
        Code is licensed under <a href="https://www.gnu.org/licenses/agpl-3.0.fr.html">AGPL</a>.
    </p>

pages-navbar-login = Sign in
pages-navbar-logout = Sign out

pages-mixins-actions-do = Do it!
pages-mixins-actions-delegate = Delegate it!
pages-mixins-actions-postpone = Mark it as actionable!
pages-mixins-actions-file = File it!
pages-mixins-actions-incubate = Incubate it for a later time.
pages-mixins-actions-eliminate = Eliminate it!
pages-mixins-actions-reclaim = Reclaim it!
pages-mixins-actions-assign = Assign it!
pages-mixins-actions-schedule = Schedule it!
pages-mixins-actions-projectify = Make it a project!
pages-mixins-list-of-tasks-display-title = Display task
pages-mixins-list-of-tasks-display-label = View
pages-mixins-list-of-tasks-postpone-title = Mark task as actionable
pages-mixins-list-of-tasks-postpone-label = Next
pages-mixins-list-of-tasks-update-title = Edit task
pages-mixins-list-of-tasks-update-label = Edit

pages-modal-close = close

pages-projects-create-title = Create new project
pages-projects-create-short-name-label = Short name
pages-projects-create-short-name-help = Used for badges wherever the name is too long to be displayed (max. { $max }).
pages-projects-create-name-label = Name
pages-projects-create-name-help = The full name of the project (max. { $max }).
pages-projects-create-submit = Create
pages-projects-create-cancel = Cancel
pages-projects-create-missing-id = You must provide an ID!
pages-projects-create-missing-name = You must provide a name!
pages-projects-create-missing-short-name = You must provide a short name!
pages-projects-create-project-already-exists = Project already exists!
pages-projects-create-project-created = Project created!

pages-projects-display-actionable-tasks-title = Actionable tasks
pages-projects-display-actionable-tasks-empty =
    There are no actionable tasks for this project.
    Please select one in the list of incubated tasks.
pages-projects-display-incubated-tasks-title = Incubated tasks
pages-projects-display-incubated-tasks-empty =
    There are no incubated tasks for this project.
    You can capture new tasks.
pages-projects-display-nothing-to-do-html =
    <p>Congratulations! There are no tasks on this project left to be done.</p>
    <p>
        If the project is not done yet, you can capture new tasks
        or you can consider it done and archive it.
    </p>
pages-projects-display-done-tasks-title = Tasks already done
pages-projects-display-done-tasks-empty = No task has yet been done for this project.
pages-projects-display-project-not-found = The project you are looking for does not exist!

pages-projects-list-title = List of projects
pages-projects-list-empty = No project to display.
pages-projects-list-new = New project
pages-projects-list-view = View

pages-tasks-errors-task-not-found = Task not found!
pages-tasks-errors-transition-not-allowed = Transition not allowed!

pages-tasks-assign-title = Assign task to a project
pages-tasks-assign-project-id-label = Project
pages-tasks-assign-project-id-help = Name of the project to assign to.
pages-tasks-assign-submit = Assign
pages-tasks-assign-cancel = Cancel
pages-tasks-assign-missing-project-id = Missing project ID!
pages-tasks-assign-incorrect-project-id = Incorrect project ID!
pages-tasks-assign-project-not-found = Project not found!
pages-tasks-assign-success = Task assigned!


pages-tasks-capture-page-title = Capture task
pages-tasks-capture-title-placeholder = A title
pages-tasks-capture-description-placeholder = An optional description of the task
pages-tasks-capture-submit = Capture
pages-tasks-capture-cancel = Cancel
pages-tasks-capture-task-id-already-used = Task ID already exists!?
pages-tasks-capture-taks-captured = Task captured!

pages-tasks-delegate-title = Delegate task to a person
pages-tasks-delegate-person-label = Person
pages-tasks-delegate-person-placeholder = Name of the person to delegated to
pages-tasks-delegate-submit = Delegate
pages-tasks-delegate-cancel = Cancel
pages-tasks-delegate-success = Task delegated!

pages-tasks-display-title = Task's details
pages-tasks-display-assigned-to = Assigned to
pages-tasks-display-delegated-to = Delegated to
pages-tasks-display-what-next = Decide what to do next
pages-tasks-display-is-actionable = Is it actionable?
pages-tasks-display-yes = Yes
pages-tasks-display-no = No
pages-tasks-display-conditions-do = If it takes less than 2 minutes…
pages-tasks-display-conditions-delegate = If someone else can do it for you…
pages-tasks-display-conditions-projectify = If it requires multiples steps…
pages-tasks-display-conditions-postpone = Else…
pages-tasks-display-conditions-assign = If it is part of a project…
pages-tasks-display-conditions-schedule = If it has to be done at a later time…
pages-tasks-display-conditions-incubate = If you want to do it someday…
pages-tasks-display-conditions-file = If you want to keep it for reference…
pages-tasks-display-conditions-eliminate = Else…
pages-tasks-display-no-action = Nothing more can be done with this task!

pages-tasks-do-success = Task marked as done!

pages-tasks-eliminate-success = Task eliminated!

pages-tasks-file-success = Task filed!

pages-tasks-inbox-title = Inbox
pages-tasks-inbox-empty-html =
    <p>
        Your inbox is empty!
        <br />
        Find the next tasks to do on
        <a href="{ $link_next }">
            <span>the next page</span>
                <span class="icon-text">
                    <span class="icon">
                        <span class="fas fa-chevron-circle-right"></span>
                    </span>
                </span>
            </span>
        </a>
    </p>

pages-tasks-incubate-success = Task incubated!

pages-tasks-index-title = Welcome to { -project-name }!
pages-tasks-index-subtitle = A task-management system.
pages-tasks-index-introduction-html =
    The heartbeat of GTD is <strong>five simple steps</strong> that apply order to chaos
    and provide you the space and structure to be more creative, strategic
    and focused.
pages-tasks-index-capture-title = Capture — collect what has your attention
pages-tasks-index-capture-description-html =
    Use an in-tray, notepad, digital list or voice recorder to capture
    everything that has your attention.
    <br />
    Little, big, personal and professional — all your to-do's, projects,
    things to handle or finish.
pages-tasks-index-clarify-title = Clarify — process what it means
pages-tasks-index-clarify-description-html =
    Take everything that you capture and ask; is it actionable?
    <br />
    If no, then trash it, incubate it, or file it as reference.
    <br />
    If yes, decide the very next action required. If it will take less
    than two minutes, do it now. If not, delegate it if you can; or put
    it on a list to do when you can.
pages-tasks-index-organize-title = Organize — put it where it belongs
pages-tasks-index-organize-description-html =
    Put action reminders on the right lists. For example, create lists for
    the apropriate categories — calls to make, errands to run, emails to send, etc.
pages-tasks-index-reflect-title = Reflect — review frequently
pages-tasks-index-reflect-description-html =
    Look over your lists as often as necessary to trust your choices about
    what to do next. Do a weekly review to get clear, get current and creative.
pages-tasks-index-engage-title = Engage — simply do
pages-tasks-index-engage-description-html =
    Use your system to take appropriate actions with confidence.

pages-tasks-next-title = Next
pages-tasks-next-empty-html =
    <p>
        Congratulations! Your list of things to do is empty!
        <br />
        Reflect and review all your
        <a href="{ $url_waiting }">
            <span>waiting</span>
            <span class="icon-text"><span class="icon"><span class="fas fa-coffee"></span></span></span>
        </a>,
        <a href="{ $url_scheduled }">
            <span>scheduled</span>
            <span class="icon-text"><span class="icon"><span class="fas fa-calendar"></span></span></span>
        </a> and
        <a href="{ $url_someday }">
            <span>someday</span>
            <span class="icon-text"><span class="icon"><span class="fas fa-umbrella"></span></span></span>
        </a>
        lists to find out what to do next.
    </p>

pages-tasks-postpone-success = Task postponed!

pages-tasks-organize-title = Organize
pages-tasks-organize-empty = No task to display. Change the filter or capture new ones!

pages-tasks-reclaim-success = Task reclaimed!

pages-tasks-schedule-title = Schedule task on a later date
pages-tasks-schedule-date-label = Date
pages-tasks-schedule-date-help = Date on which the task is scheduled to be done.
pages-tasks-schedule-submit = Schedule
pages-tasks-schedule-cancel = Cancel
pages-tasks-schedule-success = Task scheduled!

pages-tasks-scheduled-title = Scheduled
pages-tasks-scheduled-empty = You have no tasks scheduled.

pages-tasks-someday-title = Incubated tasks
pages-tasks-someday-no-task = You have no future tasks. Capture new ones!

pages-tasks-update-page-title = Update a task
pages-tasks-update-title-placeholder = A title
pages-tasks-update-description-placeholder = An optional description
pages-tasks-update-submit = Updated
pages-tasks-update-cancel = Cancel
pages-tasks-update-success = Task updated!

pages-tasks-waiting-title = Delegated tasks
pages-tasks-waiting-no-task = You have no task delegated to other persons.
