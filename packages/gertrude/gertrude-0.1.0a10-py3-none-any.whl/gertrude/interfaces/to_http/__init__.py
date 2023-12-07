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

from http import HTTPStatus as HTTP
from typing import Any, Protocol


class Headers:
    def __init__(self, status_code: int, values: dict[str, str]) -> None:
        self.status_code = status_code
        self.values = values

    def success(self, message: str) -> None:
        pass

    def failure(self, message: str) -> None:
        pass


class MessageBody(Protocol):
    def __getitem__(self, key: str) -> Any:
        ...

    def __setitem__(self, key: str, value: Any) -> None:
        ...

    def __str__(self) -> str:
        ...


class IsPresentable(Protocol):
    headers: Headers
    body: MessageBody


class EmptyBody(MessageBody):
    def __getitem__(self, key: str) -> Any:
        return None

    def __setitem__(self, key: str, value: Any) -> None:
        pass

    def __str__(self) -> str:
        return ""


class Redirection(IsPresentable):
    def __init__(self, target: str, status_code: HTTP = HTTP.SEE_OTHER) -> None:
        self.headers = Headers(status_code, {"Location": target})
        self.body = EmptyBody()
