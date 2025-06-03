import datetime as dt
from django.db import models
from rest_framework.request import Request

from timecheck.exceptions import (
    InvalidClientDatetimeField,
    InvalidServerDatetimeField,
    NoUpdate,
)
from timecheck.types import MissingAction
from timecheck.settings import conf
import logging

from timecheck.utils import normalize_dt, parse_dt


logger = logging.getLogger(__name__)


class TimeCheckPrivate:
    """Builds a set of instructions on how to interpret client and server timestamps.
    Initialization will always raise an error if the server timestamp is missing.
    Errors for missing client timestamps can be configured."""

    _missing_action: MissingAction

    def __init__(
        self,
        request: Request,
        instance: models.Model | None = None,
        server_timestamp: dt.datetime | None = None,
        client_timestamp: dt.datetime | None = None,
        header_field: str | None = None,
        body_field: str | None = None,
        instance_field: str | None = None,
        missing_action: MissingAction | None = None,
        noupdate_code: int | None = None,
        dt_fmt: str | None = None,
        raise_exception: bool | None = None,
    ):
        self.request = request
        self._header_field = header_field or conf["header_field"]
        self._body_field = body_field or conf["body_field"]
        self._instance_field = instance_field or conf["instance_field"]
        self._noupdate_code = noupdate_code or conf["noupdate_code"]
        self._missing_action = missing_action or conf["missing_action"]
        self._dt_fmt = dt_fmt or conf["dt_fmt"]
        self._raise_exception = raise_exception or conf["raise_exception"]
        logger.debug(f"raise_exception={raise_exception}, {conf['raise_exception']}")
        self.client_timestamp = client_timestamp

        if server_timestamp:
            self.server_timestamp = normalize_dt(server_timestamp, self._dt_fmt)
        elif self._instance_field and hasattr(instance, self._instance_field):
            val = getattr(instance, self._instance_field)
            if isinstance(val, dt.datetime):
                self.server_timestamp = normalize_dt(val, self._dt_fmt)
        else:
            raise InvalidServerDatetimeField(
                self._instance_field or "No instance field",
                instance,
            )

        if not self.client_timestamp:
            header_str = self.request.headers.get(self._header_field, None)
            body_str = self.request.data.get(self._body_field, None)
            if header_str:
                try:
                    self.client_timestamp = parse_dt(header_str)
                except Exception:
                    raise InvalidClientDatetimeField(self._header_field, header_str)
            elif body_str:
                try:
                    self.client_timestamp = parse_dt(body_str)
                except Exception:
                    raise InvalidClientDatetimeField(self._body_field, body_str)

    def check_get(self):
        """Raises a drf exception `NoUpdate` which provides details that there is no need to give data back to the user."""
        logger.debug(
            f"Checking get: client={self.client_timestamp}, server={self.server_timestamp}"
        )
        if not self.client_timestamp:
            if self._missing_action == "noupdate":
                if self._raise_exception:
                    raise NoUpdate(self.request.method, self._noupdate_code)
                else:
                    return False
        elif self.client_timestamp >= self.server_timestamp:
            if self._raise_exception:
                raise NoUpdate(self.request.method, self._noupdate_code)
            else:
                return False
        return True

    def check_update(self):
        """Raises a drf exception `NoUpdate` which provides details that there is no need to update the server."""
        logger.debug(
            f"Checking update: client={self.client_timestamp}, server={self.server_timestamp}"
        )
        if not self.client_timestamp:
            if self._missing_action == "noupdate":
                if self._raise_exception:
                    raise NoUpdate(self.request.method, self._noupdate_code)
                else:
                    return False
        elif self.client_timestamp <= self.server_timestamp:
            if self._raise_exception:
                raise NoUpdate(self.request.method, self._noupdate_code)
            else:
                return False
