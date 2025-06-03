from django.urls import path

from example_app.views import View

urlpatterns = [path("", View.as_view())]
