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

from typing import Iterator, Optional

import requests
from bles import Event
from bles import EventStore as EventStoreInterface
from bles.utils import event_from_string, event_to_string


class HttpEventStore(EventStoreInterface):
    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__stream: str = ""
        self.__session = requests.Session()

    def record(self, events: list[Event]) -> None:
        s = requests.Session()
        data = "\n".join([event_to_string(e) for e in events])
        with s.post(self.__url, headers=None, data=data) as resp:
            if resp.status_code != 201:
                raise Exception(f"[{resp.status_code}] {resp.text}")
        return None

    def for_stream(self, name: str) -> "HttpEventStore":
        self.__stream = name
        return self

    def read(self, start: int = 1, follow: bool = False) -> Iterator[Event]:
        url = self.__build_url(start)
        headers = {}
        if follow:
            headers = {"X-Stream": "1"}

        with self.__session.get(url, headers=headers, stream=follow) as r:
            if r.status_code != 200:
                raise RuntimeError(
                    "An error occurred while reading events! "
                    f"[status_code=`{r.status_code}`, url=`{url}`, follow=`{follow}`]"
                )

            for line in r.iter_lines():
                string = line.decode().strip()
                if string:
                    yield event_from_string(string)

    def __build_url(self, start: Optional[int] = None) -> str:
        url = self.__url
        if self.__stream:
            url = f"{url}/{self.__stream}"
        if start is not None:
            url = f"{url}?start={start}"
        return url

    def last(self) -> Optional[Event]:
        raise NotImplementedError()
