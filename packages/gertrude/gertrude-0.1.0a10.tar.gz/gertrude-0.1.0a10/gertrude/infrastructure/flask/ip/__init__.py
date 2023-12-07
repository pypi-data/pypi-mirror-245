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

from flask import Blueprint, flash, request, session, url_for

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import presenter_to_response
from gertrude.interfaces.to_http import Redirection

blueprint = Blueprint("ip", __name__)


@blueprint.get("/login")
@presenter_to_response
def login() -> Any:
    if not authorized():
        flash("Error authenticating with IP.", "error")
        return Redirection(url_for("auth.login"))

    session["user_id"] = "00000000-0000-0000-0000-000000000000"

    flash("Success authenticating with IP.", "success")
    return Redirection(url_for("auth.redirect"))


def authorized() -> bool:
    authorized_ip = services.get_settings().AUTHORIZED_IP
    client_ip = request.headers.get("X-Remote-IP", request.remote_addr) or ""
    return client_ip.startswith(authorized_ip.rstrip("*"))
