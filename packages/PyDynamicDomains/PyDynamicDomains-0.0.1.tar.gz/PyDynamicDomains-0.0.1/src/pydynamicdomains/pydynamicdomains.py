
from dataclasses import dataclass
from requests import auth

import dataclasses
import requests
import socket


@dataclass
class DynamicRecord:
    hostname: str
    password: str
    update_url_base: str
    user_agent: str
    username: str
    _current_ip: str = dataclasses.field(default='')
    _update_url: str = dataclasses.field(default='')

    @property
    def current_ip(self) -> str:
        return self._current_ip

    @current_ip.setter
    def current_ip(self, check_ip_url: str):
        self._current_ip = requests.get(check_ip_url).content.decode()

    @property
    def update_url(self) -> str:
        return self._update_url

    @update_url.setter
    def update_url(self, myip: str) -> None:
        self._update_url = f"{self.update_url_base}?hostname={self.hostname}&myip={myip}"

    def update_dynamic_record(self) -> str:
        response = "unchanged"
        if self.current_ip != socket.gethostbyname(self.hostname):
            basic_auth = auth.HTTPBasicAuth(username=self.username, password=self.password)
            headers: dict = {'User-Agent': self.user_agent,
                             'Host': self.update_url.split("/")[2]}
            response = requests.post(url=self.update_url, headers=headers, auth=basic_auth).content.decode()
        return response


