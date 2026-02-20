from django.urls import path, include
from django.http import HttpResponse
from card_game.views import deck_list, deck_detail, shuffle_deck


def home(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path("", deck_list),
    path("deck/<int:deck_id>/", deck_detail),
    path("shuffle_deck/<int:deck_id>/", shuffle_deck),
]
