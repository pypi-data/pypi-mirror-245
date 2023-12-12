from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    from .bet import Bet
    from .cards import Card, Suit


class PlayerStrategy(Protocol):
    """Dictates a strategy for a bot.

    If you inherit from this class, then the only methods that have to be implemented
    are `make_move` and `make_bet`. In these methods, you must obey the rules of whist
    (this will be checked). All other methods don't expect any return value, and are
    only there so that your strategy can monitor the progress of the game.

    See the docstrings of each method for more information.
    """

    name: str

    def notify_round_start(
        self,
        hand: list[Card],
        trump_suit: Suit,
        player_id: int,
        revealed_card: Card,
        number_of_players: int,
    ) -> None:
        """Notifies when a round is about to start (i.e. cards have been dealt)."""
        return

    @abstractmethod
    def make_move(self, allowed_cards: list[Card]) -> Card:
        """Return the Card to play on this move. Must be one of `allowed_cards`."""

    def notify_new_move(self, player_id: int, card: Card) -> None:
        """Notify that `player_id` just played `card`."""
        return

    @abstractmethod
    def make_bet(self, disallowed_bet: Optional[int] = None) -> Bet:
        """Return a Bet, with number_of_tricks different to `disallowed_bet`."""

    def notify_new_bet(self, player_id: int, bet: Bet) -> None:
        """Notify that `player_id` made a bet `bet`."""
        return

    def notify_trick_won(self, player_id: int) -> None:
        """Notify that a trick has just been won by `player_id`."""
        return

    def notify_new_trick(self, player_id: int) -> None:
        """Notify that a new trick is about to start, starting with `player_id`."""
        return

    def notify_round_end(self, results: list[tuple[int, int]]) -> None:
        """Notify that the round has ended.

        Can be used for teardown code.
        """
        return
