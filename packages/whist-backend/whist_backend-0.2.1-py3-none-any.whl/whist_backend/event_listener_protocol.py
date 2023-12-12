from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, Protocol

from .cards import Card, Suit

if TYPE_CHECKING:
    from .bet import Bet
    from .round_simulator import _Player


class WhistEventListener(Protocol):
    def notify_round_start(
        self,
        revealed_card: Card,
        trump_suit: Suit,
        hand_size: int,
        players: list[_Player],
    ) -> None:
        """Called when a new round starts."""
        return None

    def notify_card_played(self, player: _Player, played_card: Card) -> None:
        """Called when a player plays any card."""
        return None

    def notify_trick_won(self, player: _Player) -> None:
        """Called when a trick is won."""
        return None

    def notify_bets_made(self, bets: Iterator[tuple[_Player, Bet]]) -> None:
        """Called when all bets have been finalised."""
        return None

    def notify_new_trick(self, player_id: int) -> None:
        """Called when a trick is about to start (starting with `player_id`)."""
        return None
