from django.db import models
from rest_framework import exceptions

from timecheck.settings import conf


class InvalidServerDatetimeField(exceptions.APIException):
    status_code = 500

    def __init__(self, field_name: str, val: models.Model | object, code: str | int):
        if isinstance(val, models.Model):
            fields = {f.name: getattr(val, f.name) for f in val._meta.fields}
            val_info = f"<Model {val.__class__.__name__}: {fields}>"
        else:
            val_info = repr(val)

        super().__init__(
            f"InvalidServerDatetimeField: {field_name} is not a valid datetime. {val_info} is a {type(val)}",
            str(code),
        )


class InvalidClientDatetimeField(exceptions.APIException):
    status_code = 400

    def __init__(self, field_name: str, val: str, fmt: str, code: str | int):
        code = str(code)
        super().__init__(
            f"InvalidClientDatetimeField: {field_name} header {val} val is unable to be parsed with {fmt}",
            code,
        )


class NoUpdate(exceptions.APIException):
    status_code = conf["noupdate_code"]

    def __init__(self, request_method: str | None, code: str | int) -> None:
        code = str(code)
        if request_method in ["POST", "PUT"]:
            super().__init__(
                "NoUpdate: Client has submitted older data than the server. Skipping update",
                code,
            )
        elif request_method == "GET":
            super().__init__("NoUpdate: Client is already up to date", code)
        else:
            super().__init__("NoUpdate", code)
