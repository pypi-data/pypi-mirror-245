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

from abc import ABC, abstractmethod
from http import HTTPStatus as HTTP
from pathlib import Path
from typing import Any, Callable, Optional, Protocol

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2_fragments import render_block

from gertrude.interfaces.to_http import Headers, IsPresentable, MessageBody

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
)

Notifier = Callable[[str, str], None]


class Translator(Protocol):
    def __call__(self, message: str, **kwargs: Any) -> str:
        ...


class Services(ABC):
    @abstractmethod
    def url_for(self, endpoint: str, **kwargs: Any) -> str:
        ...

    @abstractmethod
    def notify(self, message: str, category: str) -> None:
        ...

    @abstractmethod
    def create_context(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def translate(self, message: str, **kwargs: Any) -> str:
        ...


class OnSuccessRedirect(Headers):
    def __init__(self, url: str, notifier: Optional[Notifier] = None) -> None:
        super().__init__(HTTP.OK, {"Content-Type": "text/html"})
        self.__url = url
        self.__notifier = notifier

    def success(self, message: str = "") -> None:
        self.status_code = HTTP.SEE_OTHER
        self.values["Location"] = self.__url
        if message and self.__notifier:
            self.__notifier(message, "success")


class OnFailureRedirect(Headers):
    def __init__(self, url: str, notifier: Optional[Notifier] = None) -> None:
        super().__init__(HTTP.OK, {"Content-Type": "text/html"})
        self.__url = url
        self.__notifier = notifier

    def failure(self, message: str = "") -> None:
        self.status_code = HTTP.SEE_OTHER
        self.values["Location"] = self.__url
        if message and self.__notifier:
            self.__notifier(message, "error")


class OnSuccessTrigger(Headers):
    def __init__(self, events: list[str], redirect: str = "") -> None:
        super().__init__(HTTP.OK, {"Content-Type": "text/html"})
        self.__events = events
        self.__redirect = redirect

    def success(self, message: str = "") -> None:
        self.values["HX-Trigger"] = ", ".join(self.__events)
        if self.__redirect:
            self.values["HX-Location"] = self.__redirect


class PugBody(MessageBody):
    def __init__(self, template: str, context: dict[str, Any]) -> None:
        self.__template, self.__fragment = self.__template_parts(template)
        self.__context = {**context}

    def __template_parts(self, template: str) -> tuple[str, str]:
        fragment = ""
        if "#" in template:
            template, fragment = template.split("#", 2)
        return f"{template}.pug" if template else "", fragment

    def __getitem__(self, key: str) -> Any:
        return self.__context[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__context[key] = value

    def __str__(self) -> str:
        if self.__fragment:
            return render_block(
                ENVIRONMENT, self.__template, self.__fragment, **self.__context
            )
        if self.__template:
            return ENVIRONMENT.get_template(self.__template).render(**self.__context)
        return ""

    def __repr__(self) -> str:
        return str(self.__context)


class HtmlPresenter(IsPresentable):
    @classmethod
    def from_template(cls, template: str, **kwargs: Any) -> "HtmlPresenter":
        return cls(
            Headers(HTTP.OK, {"Content-Type": "text/html"}), PugBody(template, kwargs)
        )

    def __init__(self, headers: Headers, body: PugBody) -> None:
        self.headers = headers
        self.body = body
