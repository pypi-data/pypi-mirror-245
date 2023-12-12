from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar

from .cards import Card, Suit, new_shuffled_deck
from .event_listener_protocol import WhistEventListener

if TYPE_CHECKING:
    from .bet import Bet
    from .player_strategy_protocol import PlayerStrategy


T = TypeVar("T")


class _Player:
    """This is used to ensure that the rules of whist are obeyed by the
    :class:`whist_backend.player_strategy_protocol.PlayerStrategy`s.
    """

    def __init__(
        self,
        strategy: PlayerStrategy,
        hand: list[Card],
        revealed_card: Card,
        player_id: int,
        number_of_players: int,
    ) -> None:
        self.strategy = strategy
        self.strategy.notify_round_start(
            hand, revealed_card.suit, player_id, revealed_card, number_of_players
        )
        self.hand = hand
        self.played_cards: list[Card] = []
        self.player_id = player_id
        self.tricks_won = 0

    def make_move(self, initial_suit: Optional[Suit]) -> Card:
        allowed_cards = self.get_allowed_cards(initial_suit)
        picked_card = self.strategy.make_move(allowed_cards)
        assert picked_card in allowed_cards, (
            f"{self.strategy.name} picked an invalid card (picked {picked_card} which"
            f"is not one of {allowed_cards})."
        )
        self.played_cards.append(picked_card)
        self.hand.remove(picked_card)
        return picked_card

    def get_allowed_cards(self, initial_suit: Optional[Suit]) -> list[Card]:
        if cards_of_initial_suit := [
            card for card in self.hand if card.suit == initial_suit
        ]:
            return cards_of_initial_suit
        else:
            return self.hand

    def make_bet(self, disallowed_bet: Optional[int] = None) -> Bet:
        bet = self.strategy.make_bet(disallowed_bet)
        assert (
            bet.number_of_tricks != disallowed_bet
        ), f"{self.strategy.name} made an invalid bet."
        return bet

    def notify_trick_won(self, player_id: int) -> None:
        if player_id == self.player_id:
            self.tricks_won += 1
        self.strategy.notify_trick_won(player_id)

    def __str__(self) -> str:
        cards_left = ",".join(str(card) for card in self.hand)
        cards_played = ",".join(str(card) for card in self.played_cards)
        return f"{self.strategy.name}: hand {cards_left}" + (
            f" (played {cards_played})" if cards_played else ""
        )


def deal_hands(
    number_of_players: int, hand_size: int, deck: list[Card]
) -> list[list[Card]]:
    return [[deck.pop() for _ in range(hand_size)] for _ in range(number_of_players)]


def determine_trump_suit_and_hand_sizes(card: Card) -> tuple[Suit, int]:
    trump_suit = card.suit
    card_value = card.rank.value
    if card_value < 5:
        return trump_suit, 10 - card_value
    elif card_value > 10:
        return trump_suit, 21 - card_value
    else:
        return trump_suit, card_value


def cyclic_shift(items: list[T], shift_amount: int) -> list[T]:
    shift_amount %= len(items)
    return items[shift_amount:] + items[:shift_amount]


def find_trick_winner(
    cards_and_players: list[tuple[_Player, Card]], trump_suit: Suit, initial_suit: Suit
) -> _Player:
    trump_suit_moves = [
        move for move in cards_and_players if move[1].suit == trump_suit
    ]
    initial_suit_moves = [
        move for move in cards_and_players if move[1].suit == initial_suit
    ]
    if trump_suit_moves:
        return max(trump_suit_moves, key=lambda move: move[1].rank)[0]
    else:
        return max(initial_suit_moves, key=lambda move: move[1].rank)[0]


class RoundSimulator:
    def __init__(
        self,
        strategies: list[PlayerStrategy],
        *,
        event_listeners: Optional[list[WhistEventListener]] = None,
    ) -> None:
        deck = new_shuffled_deck()
        revealed_card = deck.pop()
        self.trump_suit, self.hand_size = determine_trump_suit_and_hand_sizes(
            revealed_card
        )
        number_of_players = len(strategies)
        hands = deal_hands(number_of_players, self.hand_size, deck)
        self.players = [
            _Player(strategy, hand, revealed_card, player_id, number_of_players)
            for player_id, (strategy, hand) in enumerate(zip(strategies, hands))
        ]
        self.next_starting_player = 0
        self.event_listeners = event_listeners or []
        for event_listener in self.event_listeners:
            event_listener.notify_round_start(
                revealed_card, self.trump_suit, self.hand_size, self.players
            )

    def play_round(self) -> list[tuple[PlayerStrategy, int]]:
        bets = self.gather_bets_for_round(self.players)
        for _ in range(self.hand_size):
            self.play_trick()
        results = [
            (player.strategy, bet.compute_score(player.tricks_won))
            for player, bet in zip(self.players, bets)
        ]
        for player in self.players:
            player.strategy.notify_round_end(
                [(i, score) for i, (_, score) in enumerate(results)]
            )
        return results

    def make_move_on_player(
        self, player: _Player, initial_suit: Optional[Suit]
    ) -> Card:
        picked_card = player.make_move(initial_suit)
        for other_player in self.players:
            other_player.strategy.notify_new_move(player.player_id, picked_card)
        for event_listener in self.event_listeners:
            event_listener.notify_card_played(player, picked_card)
        return picked_card

    def on_trick_win(self, player: _Player) -> None:
        for other_player in self.players:
            other_player.notify_trick_won(player.player_id)
        self.next_starting_player = player.player_id
        for event_listener in self.event_listeners:
            event_listener.notify_trick_won(player)

    def ask_player_for_bet(
        self, player: _Player, disallowed_bet: Optional[int] = None
    ) -> Bet:
        bet = player.make_bet(disallowed_bet)
        for other_player in self.players:
            other_player.strategy.notify_new_bet(player.player_id, bet)
        return bet

    def gather_bets_for_round(self, player_order: list[_Player]) -> list[Bet]:
        bets = [self.ask_player_for_bet(player) for player in player_order[:-1]]
        disallowed_bet_for_last_player = self.hand_size - sum(
            map(lambda bet: bet.number_of_tricks, bets)
        )
        bets.append(
            self.ask_player_for_bet(player_order[-1], disallowed_bet_for_last_player)
        )
        for event_listener in self.event_listeners:
            event_listener.notify_bets_made(zip(player_order, bets))
        return bets

    def play_trick(self) -> None:
        for player in self.players:
            player.strategy.notify_new_trick(self.next_starting_player)
        for event_listener in self.event_listeners:
            event_listener.notify_new_trick(self.next_starting_player)
        player_order = cyclic_shift(self.players, self.next_starting_player)
        cards_played = [self.make_move_on_player(player_order[0], None)]
        initial_suit = cards_played[0].suit
        cards_played.extend(
            self.make_move_on_player(player, initial_suit)
            for player in player_order[1:]
        )
        trick_winner = find_trick_winner(
            list(zip(player_order, cards_played)), self.trump_suit, initial_suit
        )
        self.on_trick_win(trick_winner)
