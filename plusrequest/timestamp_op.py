import datetime as dt
from django.db import models
from rest_framework.request import Request

from plusrequest.exceptions import (
    InvalidClientDatetimeField,
    InvalidServerDatetimeField,
    NoUpdate,
)
from plusrequest.settings import conf
from plusrequest.types import MissingAction


class TimestampOp:
    """Builds a set of instructions on how to interpret client and server timestamps.
    Initialization will always raise an error if the server timestamp is missing.
    Errors for missing client timestamps can be configured."""

    _missing_action: MissingAction

    def __init__(self, parent: Request):
        self.parent = parent

    def __call__(
        self,
        instance: models.Model | None = None,
        server_timestamp: dt.datetime | None = None,
        client_timestamp: dt.datetime | None = None,
        header_field: str | None = None,
        body_field: str | None = None,
        instance_field: str | None = None,
        missing_action: MissingAction | None = None,
        noupdate_code: str | None = None,
        datetime_format: str | None = None,
    ):
        self._header_field = header_field or conf.header_timestamp_field
        self._body_field = body_field or conf.body_timestamp_field
        self._instance_field = instance_field or conf.instance_timestamp_field
        self._noupdate_code = noupdate_code or conf.noupdate_code
        self._missing_action = missing_action or conf.missing_action
        self._datetime_format = datetime_format or conf.datetime_format
        self.client_timestamp = client_timestamp

        if not server_timestamp and hasattr(instance, self._instance_field):
            self.server_timestamp = getattr(instance, self._instance_field)
        if not isinstance(server_timestamp, dt.datetime):
            raise InvalidServerDatetimeField(
                self._instance_field, server_timestamp, 500
            )

        if not self.client_timestamp:
            header_str = self.parent.headers.get(self._header_field, None)
            body_str = self.parent.data.get(self._body_field, None)
            if header_str:
                try:
                    self.client_timestamp = dt.datetime.strptime(
                        header_str, self._datetime_format
                    )
                except Exception:
                    raise InvalidClientDatetimeField(
                        self._header_field, header_str, self._datetime_format, 400
                    )
            elif body_str:
                try:
                    self.client_timestamp = dt.datetime.strptime(
                        body_str, self._datetime_format
                    )
                except Exception:
                    raise InvalidClientDatetimeField(
                        self._body_field, body_str, self._datetime_format, 400
                    )
        return self

    def raise_get(
        self, code: str | int | None = None, missing_action: MissingAction | None = None
    ):
        """Raises a drf exception `NoUpdate` which provides details that there is no need to give data back to the user."""
        code = code or self._noupdate_code
        missing_action = missing_action or self._missing_action
        if not self.client_timestamp and missing_action == "noupdate":
            raise NoUpdate(self.parent.method, code)
        if self.client_timestamp >= self.server_timestamp:
            raise NoUpdate(self.parent.method, code)

    def raise_update(
        self, code: str | int | None = None, missing_action: MissingAction | None = None
    ):
        """Raises a drf exception `NoUpdate` which provides details that there is no need to update the server."""
        code = code or self._noupdate_code
        missing_action = missing_action or self._missing_action
        if not self.client_timestamp and missing_action == "noupdate":
            raise NoUpdate(self.parent.method, code)
        if self.client_timestamp < self.server_timestamp:
            raise NoUpdate(self.parent.method, code)
