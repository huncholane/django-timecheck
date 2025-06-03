from django.db import models
from rest_framework import exceptions

from timecheck.settings import conf


class InvalidServerDatetimeField(exceptions.APIException):
    status_code = 500

    def __init__(self, field_name: str, val: models.Model | object):
        if isinstance(val, models.Model):
            fields = {f.name: getattr(val, f.name) for f in val._meta.fields}
            val_info = f"<Model {val.__class__.__name__}: {fields}>"
        else:
            val_info = repr(val)
        super().__init__(
            f"InvalidServerDatetimeField: {field_name} is not a valid datetime. {val_info} is a {type(val)}",
        )


class InvalidClientDatetimeField(exceptions.APIException):
    status_code = 400

    def __init__(self, field_name: str, val: str):
        super().__init__(
            f"InvalidClientDatetimeField: {field_name} header {val}",
        )


class NoUpdate(exceptions.APIException):
    status_code = conf["noupdate_code"]

    def __init__(self, request_method: str | None, code: int) -> None:
        self.status_code = code
        if request_method in ["POST", "PUT"]:
            super().__init__(
                "NoUpdate: Client has submitted older data than the server. Skipping update",
            )
        elif request_method == "GET":
            super().__init__("NoUpdate: Client is already up to date")
        else:
            super().__init__("NoUpdate")
