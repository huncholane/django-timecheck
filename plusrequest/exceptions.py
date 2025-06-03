from typing import Any
from rest_framework import exceptions


class InvalidServerDatetimeField(exceptions.APIException):
    def __init__(self, field_name: str, val: Any, code: str | int):
        super().__init__(
            f"{field_name} is not a valid datetime. {val} is a {type(val)}", str(code)
        )


class InvalidClientDatetimeField(exceptions.APIException):
    def __init__(self, field_name: str, val: str, fmt: str, code: str | int):
        code = str(code)
        super().__init__(
            f"{field_name} header {val} val is unable to be parsed with {fmt}",
            code,
        )


class NoUpdate(exceptions.APIException):
    def __init__(self, request_method: str | None, code: str | int) -> None:
        code = str(code)
        if request_method in ["POST", "PUT"]:
            super().__init__(
                "Client has submitted older data than the server. Skipping update", code
            )
        elif request_method == "GET":
            super().__init__("Client is already up to date", code)
        else:
            super().__init__("No update", code)
