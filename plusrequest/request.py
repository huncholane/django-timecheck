from typing import (
    TYPE_CHECKING,
)
from django.http import HttpRequest
from rest_framework.request import Request

from plusrequest.meta import Meta
from plusrequest.timestamp_op import TimestampOp


class PlusRequest(Request, HttpRequest):
    if TYPE_CHECKING:
        META: Meta

    @property
    def top_builder(self):
        """A property that runs the `__call__` method for `TimestampOp` which initializes from kwargs first, then `PlusRequest` app settings.

        ```python
        def view(request: PlusRequest):
            if request.top_builder(<configure>).client_is_newer:
                return Response("Client doesn't need anything")
            ...
            return Response(data)
        ```"""
        return TimestampOp(self)
