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

import logging

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.aliases import blueprint as aliases
from gertrude.infrastructure.flask.auth import blueprint as auth
from gertrude.infrastructure.flask.projects import blueprint as projects
from gertrude.infrastructure.flask.tasks import blueprint as tasks
from gertrude.infrastructure.settings import WsgiSettings


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    configure_logging(settings)

    app = Flask(
        __name__,
        static_folder="./static/",
        static_url_path="/resources",
        template_folder="./templates/",
    )

    CORS(app)
    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        DATA_DSN=settings.DATA_DSN,
        PROJECTION_DSN=settings.PROJECTION_DSN,
        DEBUG_SQL=settings.DEBUG_SQL,
        SESSION_COOKIE_SECURE=not app.config["DEBUG"],
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if settings.PROXIED:
        app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    app.register_blueprint(aliases, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(projects, url_prefix="/projects")

    app.auth_links = []  # type: ignore[attr-defined]
    app.register_blueprint(auth, url_prefix="/auth")

    if settings.AUTHORIZED_IP:
        from gertrude.infrastructure.flask.ip import blueprint as ip

        app.register_blueprint(ip, url_prefix="/auth/ip")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "ip.login", "label": "IP"}
        )

    app.teardown_appcontext(services.close_sessions)

    return app


def configure_logging(settings: WsgiSettings) -> None:
    level = logging.WARN
    str_fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S %z"

    if settings.DEBUG:
        # Extra noisy!
        # str_fmt = str_fmt + " (%(pathname)s:%(lineno)d)"
        level = logging.DEBUG

    logging.basicConfig(format=str_fmt, level=level, datefmt=date_fmt)
