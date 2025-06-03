from typing import Union
from rest_framework.request import Request
from rest_framework.response import Response
from example_app.models import Post
from plusrequest.request import PlusRequest
from rest_framework.views import APIView


class View(APIView):
    def get(self, request: PlusRequest):
        instance = Post.objects.all().first()
        if instance:
            request.top_builder(instance=instance).raise_get()
        return Response(
            {
                "CONTENT_LENGTH": request.META.get("CONTENT_LENGTH"),
                "HTTP_ACCEPT": request.META.get("HTTP_ACCEPT"),
            }
        )

    def put(self, request: PlusRequest):
        instance = Post.objects.filter(request.data.get("id", None)).first()
        if instance:
            request.top_builder(instance=instance).raise_update()
        return Response({"port": request.META.get("SERVER_PORT")})
