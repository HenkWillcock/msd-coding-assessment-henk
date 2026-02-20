from django.db import models, transaction
from django.db.models import Q
import random


class Deck(models.Model):
    """A collection of cards. The table itself has no extra fields; all
    information lives on the related Card objects.  A utility method for
    shuffling the deck is provided.
    """

    def __str__(self):
        return f"Deck {self.pk}"

    def shuffle(self):
        """Randomise card positions within this deck.

        Uses a two-pass approach with temporary large integers to avoid
        unique constraint violations during the shuffle.
        """
        with transaction.atomic():
            cards = list(self.cards.all())
            random.shuffle(cards)

            # First pass: assign temporary large positive positions to avoid conflicts
            for index, card in enumerate(cards, start=1):
                card.position = 1000000 + index

            Card.objects.bulk_update(cards, ["position"])

            # Second pass: assign final positions
            for index, card in enumerate(cards, start=1):
                card.position = index

            Card.objects.bulk_update(cards, ["position"])


class PictureValue(models.TextChoices):
    ACE = "A", "Ace"
    KING = "K", "King"
    QUEEN = "Q", "Queen"
    JACK = "J", "Jack"
    JOKER = "JOKER", "Joker"


class Suit(models.TextChoices):
    HEARTS = "HEARTS", "Hearts"
    SPADES = "SPADES", "Spades"
    CLUBS = "CLUBS", "Clubs"
    DIAMONDS = "DIAMONDS", "Diamonds"


class Card(models.Model):

    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    # exactly one of the next two should be non-null
    face_value = models.IntegerField(null=True, blank=True)
    picture_value = models.CharField(
        max_length=10, choices=PictureValue.choices, null=True, blank=True
    )

    suit = models.CharField(
        max_length=10, choices=Suit.choices, null=True, blank=True
    )

    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ("deck", "position")
        constraints = [
            # Only one of face_value/picture_value should be populated
            models.CheckConstraint(
                condition=(
                    (Q(face_value__isnull=False) & Q(picture_value__isnull=True))
                    | (Q(face_value__isnull=True) & Q(picture_value__isnull=False))
                ),
                name="card_face_or_picture_exactly_one",
            ),
            # If picture_value is Joker then suit must be null;
            # otherwise suit cannot be null
            models.CheckConstraint(
                condition=(
                    (Q(picture_value=PictureValue.JOKER) & Q(suit__isnull=True))
                    | ~Q(picture_value=PictureValue.JOKER) & Q(suit__isnull=False)
                ),
                name="card_suit_required_unless_joker",
            ),
        ]

    def __str__(self):
        value = self.picture_value if self.picture_value else str(self.face_value)
        return value + (f" of {self.suit}" if self.suit else "")
