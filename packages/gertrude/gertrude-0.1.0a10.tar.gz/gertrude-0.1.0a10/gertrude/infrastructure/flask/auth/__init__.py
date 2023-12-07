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

from typing import Any

from flask import Blueprint, current_app, flash, request, session, url_for

from gertrude.infrastructure.flask.utils import presenter_to_response
from gertrude.interfaces.to_http import Redirection, as_html

blueprint = Blueprint("auth", __name__)

DEFAULT_ENDPOINT = "tasks.index"


@blueprint.get("")
@presenter_to_response
def root() -> Any:
    return Redirection(url_for(DEFAULT_ENDPOINT))


@blueprint.get("/login")
@presenter_to_response
def login() -> Any:
    session.permanent = True
    session["redirect"] = request.referrer

    auth_links = current_app.auth_links  # type: ignore[attr-defined]
    if not auth_links:
        return Redirection(url_for(DEFAULT_ENDPOINT))
    if len(auth_links) == 1:
        return Redirection(url_for(auth_links[0]["route"]))
    return as_html.HtmlPresenter.from_template("auth/login", links=auth_links)


@blueprint.get("/redirect")
@presenter_to_response
def redirect() -> Any:
    if url := session.pop("redirect", ""):
        return Redirection(url)
    return Redirection(url_for(DEFAULT_ENDPOINT))


@blueprint.get("/logout")
@presenter_to_response
def logout() -> Any:
    session.clear()
    flash("You are not logged in anymore.", "info")
    return Redirection(request.referrer or url_for(DEFAULT_ENDPOINT))
