from plusrequest.timestamp_op import TimestampOp


class PlusRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Add header device date functionality to request
        request.top_builder = TimestampOp(request)

        # Ensure the member shortcut exists
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
