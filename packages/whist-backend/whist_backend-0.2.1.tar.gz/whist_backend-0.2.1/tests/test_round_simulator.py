from itertools import chain, product
from unittest.mock import MagicMock, Mock

import pytest

from whist_backend.bet import Bet
from whist_backend.cards import Card, Rank, Suit
from whist_backend.player_strategy_protocol import PlayerStrategy
from whist_backend.round_simulator import (
    _Player,
    cyclic_shift,
    deal_hands,
    determine_trump_suit_and_hand_sizes,
    find_trick_winner,
)


class TestBet:
    @pytest.mark.parametrize(
        ["bet", "actual_result", "expected"],
        [
            (Bet(0, False), 1, -1),
            (Bet(3, False), 0, -3),
            (Bet(0, False), 0, 10),
            (Bet(2, False), 2, 12),
            (Bet(0, True), 1, -8),
            (Bet(0, True), 3, -24),
            (Bet(4, True), 2, -16),
            (Bet(0, True), 0, 20),
            (Bet(1, True), 1, 22),
            (Bet(3, True), 3, 26),
        ],
    )
    def test_bet_compute_score(
        self, bet: Bet, actual_result: int, expected: int
    ) -> None:
        assert bet.compute_score(actual_result) == expected

    @pytest.mark.parametrize(
        ["bet", "expected"],
        [
            (Bet(0, False), "0"),
            (Bet(1, False), "1"),
            (Bet(3, False), "3"),
            (Bet(10, False), "10"),
            (Bet(0, True), "CONFIDENT 0"),
            (Bet(1, True), "CONFIDENT 1"),
            (Bet(3, True), "CONFIDENT 3"),
            (Bet(10, True), "CONFIDENT 10"),
        ],
    )
    def test_bet_string(self, bet: Bet, expected: str) -> None:
        assert str(bet) == expected


class TestPlayer:
    def test_make_move_and_str(self) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.make_move.side_effect = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
        ]
        strategy.name = "TestBot"
        player = _Player(strategy, hand, Card(Rank.ACE, Suit.DIAMONDS), 1, 1)
        strategy.notify_round_start.assert_called_with(
            [
                Card(Rank.ACE, Suit.SPADES),
                Card(Rank.TEN, Suit.SPADES),
                Card(Rank.TWO, Suit.CLUBS),
                Card(Rank.FOUR, Suit.DIAMONDS),
            ],
            Suit.DIAMONDS,
            1,
            Card(Rank.ACE, Suit.DIAMONDS),
            1,
        )
        player.make_move(Suit.SPADES)
        strategy.make_move.assert_called_with(
            [Card(Rank.ACE, Suit.SPADES), Card(Rank.TEN, Suit.SPADES)]
        )
        player.make_move(Suit.SPADES)
        strategy.make_move.assert_called_with([Card(Rank.TEN, Suit.SPADES)])
        assert str(player) == "TestBot: hand  2♣, 4♦ (played  A♠,10♠)"

    @pytest.mark.parametrize(
        ["card"],
        [
            (Card(Rank.ACE, Suit.SPADES),),
            (Card(Rank.TEN, Suit.SPADES),),
            (Card(Rank.TWO, Suit.CLUBS),),
            (Card(Rank.FOUR, Suit.DIAMONDS),),
        ],
    )
    def test_valid_move_no_initial_suit(self, card: Card) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.make_move.side_effect = [card]
        player = _Player(strategy, hand, Mock(), Mock(), Mock())
        player.make_move(None)

    @pytest.mark.parametrize(
        ["card", "initial_suit"],
        [
            (Card(Rank.ACE, Suit.SPADES), Suit.SPADES),
            (Card(Rank.TEN, Suit.SPADES), Suit.HEARTS),
            (Card(Rank.TWO, Suit.CLUBS), Suit.CLUBS),
            (Card(Rank.FOUR, Suit.DIAMONDS), Suit.DIAMONDS),
            (Card(Rank.FOUR, Suit.DIAMONDS), Suit.HEARTS),
        ],
    )
    def test_valid_move_with_initial_suit(self, card: Card, initial_suit: Suit) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.make_move.side_effect = [card]
        player = _Player(strategy, hand, Mock(), Mock(), Mock())
        player.make_move(initial_suit)

    def test_invalid_move_no_initial_suit(self) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.make_move.side_effect = [Card(Rank.ACE, Suit.CLUBS)]
        player = _Player(strategy, hand, Mock(), Mock(), Mock())
        with pytest.raises(AssertionError):
            player.make_move(None)

    def test_invalid_move_with_initial_suit(self) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.make_move.side_effect = [Card(Rank.ACE, Suit.SPADES)]
        player = _Player(strategy, hand, Mock(), Mock(), Mock())
        with pytest.raises(AssertionError):
            player.make_move(Suit.DIAMONDS)

    def test_str(self) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        strategy: PlayerStrategy = Mock()
        strategy.name = "TestBot"
        player = _Player(strategy, hand, Card(Rank.ACE, Suit.DIAMONDS), Mock(), 1)
        assert str(player) == "TestBot: hand  A♠,10♠, 2♣, 4♦"

    def test_make_valid_bet_no_disallowed(self) -> None:
        strategy: PlayerStrategy = Mock()
        strategy.name = "TestBot"
        strategy.make_bet.side_effect = [Bet(0, False)]
        player = _Player(strategy, Mock(), Mock(), Mock(), Mock())
        player.make_bet(None)

    def test_make_valid_bet(self) -> None:
        strategy: PlayerStrategy = Mock()
        strategy.name = "TestBot"
        strategy.make_bet.side_effect = [Bet(0, False)]
        player = _Player(strategy, Mock(), Mock(), Mock(), Mock())
        player.make_bet(1)

    def test_make_invalid_bet(self) -> None:
        strategy: PlayerStrategy = Mock()
        strategy.name = "TestBot"
        strategy.make_bet.side_effect = [Bet(0, False)]
        player = _Player(strategy, Mock(), Mock(), Mock(), Mock())
        with pytest.raises(AssertionError):
            player.make_bet(0)

    @pytest.mark.parametrize(
        ["initial_suit", "expected"],
        [
            (Suit.SPADES, [Card(Rank.ACE, Suit.SPADES), Card(Rank.TEN, Suit.SPADES)]),
            (
                Suit.HEARTS,
                [
                    Card(Rank.ACE, Suit.SPADES),
                    Card(Rank.TEN, Suit.SPADES),
                    Card(Rank.TWO, Suit.CLUBS),
                    Card(Rank.FOUR, Suit.DIAMONDS),
                ],
            ),
            (Suit.DIAMONDS, [Card(Rank.FOUR, Suit.DIAMONDS)]),
            (Suit.CLUBS, [Card(Rank.TWO, Suit.CLUBS)]),
            (
                None,
                [
                    Card(Rank.ACE, Suit.SPADES),
                    Card(Rank.TEN, Suit.SPADES),
                    Card(Rank.TWO, Suit.CLUBS),
                    Card(Rank.FOUR, Suit.DIAMONDS),
                ],
            ),
        ],
    )
    def test_get_allowed_cards(self, initial_suit: Suit, expected: list[Card]) -> None:
        hand = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.TWO, Suit.CLUBS),
            Card(Rank.FOUR, Suit.DIAMONDS),
        ]
        player = _Player(Mock(), hand, Mock(), Mock(), Mock())
        assert player.get_allowed_cards(initial_suit) == expected

    def test_notify_trick_won(self) -> None:
        strategy: PlayerStrategy = Mock()
        player = _Player(strategy, Mock(), Mock(), 1, 1)
        player.tricks_won = MagicMock()
        player.notify_trick_won(1)
        strategy.notify_trick_won.called_once_with(1)
        player.tricks_won.__iadd__.called_once_with(1)

    def test_notify_trick_not_won(self) -> None:
        strategy: PlayerStrategy = Mock()
        player = _Player(strategy, Mock(), Mock(), 1, 1)
        player.tricks_won = MagicMock()
        player.notify_trick_won(2)
        strategy.notify_trick_won.called_once_with(2)
        player.tricks_won.__iadd__.assert_not_called()


def test_deal_hands() -> None:
    deck = [Card(rank, suit) for rank, suit in product(Rank, Suit)]
    hands = deal_hands(4, 13, deck)
    assert all(len(hand) == 13 for hand in hands)
    assert len(set(chain(*hands))) == 52


@pytest.mark.parametrize(
    ["revealed_card", "expected"],
    [
        (Card(Rank.ACE, Suit.SPADES), (Suit.SPADES, 9)),
        (Card(Rank.TEN, Suit.DIAMONDS), (Suit.DIAMONDS, 10)),
        (Card(Rank.JACK, Suit.DIAMONDS), (Suit.DIAMONDS, 10)),
        (Card(Rank.FOUR, Suit.CLUBS), (Suit.CLUBS, 6)),
        (Card(Rank.KING, Suit.HEARTS), (Suit.HEARTS, 8)),
    ],
)
def test_determine_trump_suit_and_hand_sizes(
    revealed_card: Card, expected: tuple[Suit, int]
) -> None:
    assert determine_trump_suit_and_hand_sizes(revealed_card) == expected


@pytest.mark.parametrize(
    ["input_list", "amount", "expected"],
    [
        ([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 1, [2, 3, 4, 5, 1]),
        ([1, 2, 3, 4, 5], 2, [3, 4, 5, 1, 2]),
        ([1, 2, 3, 4, 5], 3, [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], 4, [5, 1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
    ],
)
def test_cyclic_shift(input_list: list[int], amount: int, expected: list[int]) -> None:
    assert cyclic_shift(input_list, amount) == expected


CARDS_AND_PLAYERS = [
    (0, Card(Rank.ACE, Suit.SPADES)),
    (1, Card(Rank.KING, Suit.SPADES)),
    (2, Card(Rank.TEN, Suit.DIAMONDS)),
    (3, Card(Rank.ACE, Suit.DIAMONDS)),
    (4, Card(Rank.TWO, Suit.HEARTS)),
]


@pytest.mark.parametrize(
    ["trump_suit", "initial_suit", "expected"],
    [
        (Suit.SPADES, Suit.SPADES, 0),
        (Suit.DIAMONDS, Suit.HEARTS, 3),
        (Suit.HEARTS, Suit.SPADES, 4),
        (Suit.HEARTS, Suit.HEARTS, 4),
        (Suit.CLUBS, Suit.HEARTS, 4),
        (Suit.CLUBS, Suit.SPADES, 0),
    ],
)
def test_find_trick_winner(trump_suit: Suit, initial_suit: Suit, expected: int) -> None:
    assert (
        find_trick_winner(CARDS_AND_PLAYERS, trump_suit, initial_suit) == expected
    )  # type: ignore
