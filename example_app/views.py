from rest_framework.response import Response
from example_app.models import Post
from rest_framework.views import APIView

from timecheck import TimeCheck


class View(APIView):
    def get(self, request):
        instance = Post.objects.all().first()
        if instance:
            TimeCheck(request, instance).check_get()
        return Response(
            {
                "CONTENT_LENGTH": request.META.get("CONTENT_LENGTH"),
                "HTTP_ACCEPT": request.META.get("HTTP_ACCEPT"),
            }
        )

    def put(self, request):
        instance = Post.objects.all().first()
        if instance:
            TimeCheck(request, instance).check_update()
        return Response({"port": request.META.get("SERVER_PORT")})
