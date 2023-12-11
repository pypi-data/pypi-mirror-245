from dataclasses import dataclass
from datetime import datetime
from time import time
from typing import Callable, Union

from api_analytics.core import log_request
from tornado.httputil import HTTPServerRequest
from tornado.web import Application, RequestHandler


@dataclass
class Config:
    """
    Configuration for the Tornado API Analytics middleware.

    :param get_path: Optional custom mapping function that takes a request and
        returns the path stored within the request. if set, it overrides the
        default behaviour of API Analytics.
    :param get_ip_address: Optional custom mapping function that takes a request
        and returns the IP address stored within the request. If set, it
        overrides the default behaviour of API Analytics.
    :param get_hostname: Optional custom mapping function that takes a request and
        returns the hostname stored within the request. If set, it overrides
        the default behaviour of API Analytics.
    :param get_user_agent: Optional custom mapping function that takes a request
        and returns the user agent stored within the request. If set, it
        overrides the default behaviour of API Analytics.
    :param get_user_id: Optional custom mapping function that takes a request and
        returns a custom user ID stored within the request. If set, this can be
        used to track a custom user ID specific to your API such as an API key
        or client ID. If left as `None`, no custom user ID will be used, and user
        identification will rely on client IP address only.
    """

    get_path: Union[Callable[[HTTPServerRequest], str], None] = None
    get_ip_address: Union[Callable[[HTTPServerRequest], str], None] = None
    get_hostname: Union[Callable[[HTTPServerRequest], str], None] = None
    get_user_agent: Union[Callable[[HTTPServerRequest], str], None] = None
    get_user_id: Union[Callable[[HTTPServerRequest], str], None] = None


class Analytics(RequestHandler):
    """API Analytics middleware for Tornado."""

    def __init__(
        self,
        app: Application,
        res: HTTPServerRequest,
        api_key: str,
        config: Config = Config(),
    ):
        super().__init__(app, res)
        self.api_key = api_key
        self.config = config
        self.start = time()

    def prepare(self):
        self.start = time()

    def on_finish(self):
        request_data = {
            "hostname": self._get_hostname(),
            "ip_address": self._get_ip_address(),
            "path": self._get_path(),
            "user_agent": self.get_user_agent(),
            "method": self.request.method,
            "status": self.get_status(),
            "response_time": int((time() - self.start) * 1000),
            "created_at": datetime.now().isoformat(),
        }

        log_request(self.api_key, request_data, "Tornado")
        self.start = None

    def _get_path(self) -> Union[str, None]:
        if self.config.get_path:
            return self.config.get_path(self.request)
        return self.request.path

    def _get_ip_address(self) -> Union[str, None]:
        if self.config.get_ip_address:
            return self.config.get_ip_address(self.request)
        return self.request.remote_ip

    def _get_hostname(self) -> Union[str, None]:
        if self.config.get_hostname:
            return self.config.get_hostname(self.request)
        return self.request.host

    def _get_user_id(self) -> Union[str, None]:
        if self.config.get_user_id:
            return self.config.get_user_id(self.request)
        return None

    def _get_user_agent(self) -> Union[str, None]:
        if self.config.get_user_agent:
            return self.config.get_user_agent(self.request)
        elif "user-agent" in self.request.headers:
            return self.request.headers["user-agent"]
        elif "User-Agent" in self.request.headers:
            return self.request.headers["User-Agent"]
        return None
