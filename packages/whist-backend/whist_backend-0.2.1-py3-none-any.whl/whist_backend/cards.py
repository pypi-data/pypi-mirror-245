from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from random import shuffle


class Suit(Enum):
    """An enum for each card suit.

    .. automethod:: __str__
    """

    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3

    def __str__(self) -> str:
        """Return a single character representing the suit, eg `♠`."""
        return "♠♥♦♣"[self.value]


class Rank(Enum):
    """An Enum for each card rank.

    Note that ACE has value 1.

    You can use the `>` operator on Ranks.

    .. automethod:: __str__

    .. automethod:: __lt__

    .. automethod:: __gt__

    .. automethod:: __le__

    .. automethod:: __ge__
    """

    value: int

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __lt__(self, other: Rank) -> bool:
        """Given `self < other`, return `True` if `other` is strictly better."""
        if not isinstance(other, Rank):
            NotImplementedError("Ranks can only be compared to ranks.")  # type: ignore

        return self.whist_value() < other.whist_value()

    def __str__(self) -> str:
        """Return a short string representation of the rank, eg `A` or `10`."""
        if self == Rank.ACE:
            return "A"
        elif self == Rank.JACK:
            return "J"
        elif self == Rank.QUEEN:
            return "Q"
        elif self == Rank.KING:
            return "K"
        else:
            return str(self.value)

    def whist_value(self) -> int:
        return 14 if self == Rank.ACE else self.value


@dataclass(frozen=True)
class Card:
    """Represents a card object.

    This is implemented as a frozen dataclass, so magic methods such as `__hash__` and
    `__eq__` are automatically defined on it.

    .. automethod:: __str__
    """

    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        """Return a 3 character representation of the card, eg ` A♠`."""
        return f"{self.rank:>2}{self.suit}"


def new_deck() -> list[Card]:
    """Return a full, new, sorted deck of cards."""
    return [Card(rank, suit) for rank, suit in product(Rank, Suit)]


def new_shuffled_deck() -> list[Card]:
    """Return a full, new, shuffled deck of cards."""
    deck = new_deck()
    shuffle(deck)
    return deck
