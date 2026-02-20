from django.shortcuts import render, get_object_or_404, redirect
from card_game.models import Deck, Card, PictureValue, Suit



def deck_list(request):
    """List all decks in the database. If none exist, create one."""
    decks = Deck.objects.all()
    if not decks.exists():
        Deck.objects.create()
        decks = Deck.objects.all()
    return render(request, "card_game/deck_list.html", {"decks": decks})


def _populate_standard_deck(deck):
    """Populate a deck with a standard 54-card set (52 + 2 jokers)."""
    # Create 52 standard cards: 13 ranks × 4 suits
    card_data = []
    position = 1
    
    # Face value cards: 2-10
    for face_val in range(2, 11):
        for suit in [Suit.HEARTS, Suit.SPADES, Suit.CLUBS, Suit.DIAMONDS]:
            card_data.append({
                "deck": deck,
                "face_value": face_val,
                "picture_value": None,
                "suit": suit,
                "position": position,
            })
            position += 1
    
    # Picture value cards: A, K, Q, J (one per suit)
    for picture in [PictureValue.ACE, PictureValue.KING, PictureValue.QUEEN, PictureValue.JACK]:
        for suit in [Suit.HEARTS, Suit.SPADES, Suit.CLUBS, Suit.DIAMONDS]:
            card_data.append({
                "deck": deck,
                "face_value": None,
                "picture_value": picture,
                "suit": suit,
                "position": position,
            })
            position += 1
    
    # Add 2 jokers (no suit)
    for _ in range(2):
        card_data.append({
            "deck": deck,
            "face_value": None,
            "picture_value": PictureValue.JOKER,
            "suit": None,
            "position": position,
        })
        position += 1
    
    Card.objects.bulk_create([Card(**card) for card in card_data])


def deck_detail(request, deck_id):
    """Show all cards in a specific deck, ordered by position.
    If the deck is empty, populate it with a standard 54-card set."""
    deck = get_object_or_404(Deck, id=deck_id)
    
    # Populate if empty
    if not deck.cards.exists():
        _populate_standard_deck(deck)
    
    cards = deck.cards.all().order_by("position")
    return render(request, "card_game/deck_detail.html", {"deck": deck, "cards": cards})


def shuffle_deck(request, deck_id):
    """Shuffle the deck and redirect back to the detail view."""
    deck = get_object_or_404(Deck, id=deck_id)
    deck.shuffle()
    return redirect(f"/{deck_id}/deck_detail", deck_id=deck_id)
