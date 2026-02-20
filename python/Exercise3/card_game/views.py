from django.shortcuts import render, get_object_or_404
from card_game.models import Deck


def deck_list(request):
    """List all decks in the database. If none exist, create one."""
    decks = Deck.objects.all()
    if not decks.exists():
        Deck.objects.create()
        decks = Deck.objects.all()
    return render(request, "card_game/deck_list.html", {"decks": decks})


def deck_detail(request, deck_id):
    """Show all cards in a specific deck, ordered by position."""
    deck = get_object_or_404(Deck, id=deck_id)
    cards = deck.cards.all().order_by("position")
    return render(request, "card_game/deck_detail.html", {"deck": deck, "cards": cards})
