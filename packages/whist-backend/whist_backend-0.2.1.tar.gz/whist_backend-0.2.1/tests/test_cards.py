import pytest

from whist_backend.cards import Card, Rank, Suit, new_deck, new_shuffled_deck


@pytest.mark.parametrize(
    ["rank1", "rank2", "expected"],
    [
        (Rank.ACE, Rank.KING, True),
        (Rank.KING, Rank.QUEEN, True),
        (Rank.QUEEN, Rank.JACK, True),
        (Rank.JACK, Rank.TEN, True),
        (Rank.TEN, Rank.NINE, True),
        (Rank.NINE, Rank.TWO, True),
        (Rank.ACE, Rank.ACE, False),
        (Rank.KING, Rank.KING, False),
        (Rank.QUEEN, Rank.QUEEN, False),
        (Rank.TEN, Rank.TEN, False),
        (Rank.TWO, Rank.TWO, False),
        (Rank.TWO, Rank.THREE, False),
        (Rank.TEN, Rank.JACK, False),
        (Rank.JACK, Rank.QUEEN, False),
        (Rank.QUEEN, Rank.KING, False),
        (Rank.KING, Rank.ACE, False),
        (Rank.TWO, Rank.ACE, False),
    ],
)
def test_rank_inequality(rank1: Rank, rank2: Rank, expected: bool) -> None:
    assert (rank1 > rank2) is expected


@pytest.mark.parametrize(
    ["rank", "expected"],
    [
        (Rank.ACE, "A"),
        (Rank.KING, "K"),
        (Rank.QUEEN, "Q"),
        (Rank.JACK, "J"),
        (Rank.TEN, "10"),
        (Rank.THREE, "3"),
        (Rank.TWO, "2"),
    ],
)
def test_rank_string(rank: Rank, expected: str) -> None:
    assert str(rank) == expected


@pytest.mark.parametrize(
    ["suit", "expected"],
    [
        (Suit.SPADES, "♠"),
        (Suit.HEARTS, "♥"),
        (Suit.DIAMONDS, "♦"),
        (Suit.CLUBS, "♣"),
    ],
)
def test_suit_string(suit: Suit, expected: str) -> None:
    assert str(suit) == expected


@pytest.mark.parametrize(
    ["card", "expected"],
    [
        (Card(Rank.ACE, Suit.SPADES), " A♠"),
        (Card(Rank.KING, Suit.CLUBS), " K♣"),
        (Card(Rank.QUEEN, Suit.DIAMONDS), " Q♦"),
        (Card(Rank.JACK, Suit.SPADES), " J♠"),
        (Card(Rank.TEN, Suit.HEARTS), "10♥"),
        (Card(Rank.SIX, Suit.SPADES), " 6♠"),
    ],
)
def test_card_string(card: Card, expected: str) -> None:
    assert str(card) == expected


def test_deck() -> None:
    assert len(set(new_deck())) == 52
    assert len(set(new_deck() + new_deck())) == 52


def test_shuffled_deck() -> None:
    assert set(new_deck()) == set(new_shuffled_deck())
