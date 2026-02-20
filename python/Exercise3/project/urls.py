from django.urls import path
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path("", home),
]
