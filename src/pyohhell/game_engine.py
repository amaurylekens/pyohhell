#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List, Optional
from itertools import cycle
import logging

from pydecklib.card import Card, Suit
from pydecklib.deck import Deck

from src.pyohhell.player import AbstractPlayer
from src.pyohhell.game_state import (
    AbstractPointAttributionStrategy,
    GameState,
    Round,
    Value,
    Trick
)


def get_authorised_cards(
    cards: List[Card], trick_suit: Optional[Suit]
) -> List[Card]:

    """
    Determines the authorised cards a player can use based on the suit of the
    current trick.

    :param cards: A list of cards available to the player.
    :type cards: List[Card]
    :param trick_suit: The suit of the current trick.
    :type trick_suit: Optional[Suit]

    :return: A list of authorised cards.
    :rtype: List[Card]

    :Example:
        >>> hand = [
        ...     Card(Suit.HEARTS, Value.ACE),
        ...     Card(Suit.SPADES, Value.KING),
        ...     Card(Suit.HEARTS, Value.TEN)
        ... ]
        >>> get_authorised_cards(hand, Suit.HEARTS)
        [Card(Suit.HEARTS, Value.ACE), Card(Suit.HEARTS, Value.TEN)]
    """

    if trick_suit:
        trick_suit_cards = [
            card for card in cards if card.suit == trick_suit
        ]

        if trick_suit_cards:
            return trick_suit_cards

    return cards


def get_authorised_bids(
    n_cards: int, total_bid: int, last_player: bool
) -> List[int]:

    """
    Determines the authorised bids a player can make, given the number of cards
    and the total bid so far, especially considering the rule for the last
    player.

    :param n_cards: The number of cards held by the player.
    :type n_cards: int
    :param total_bid: The total bid made by other players so far.
    :type total_bid: int
    :param last_player: A boolean indicating if the player is the last to bid.
    :type last_player: bool

    :return: A list of authorised bids.
    :rtype: List[int]

    :Example:
        >>> get_authorised_bids(5, 7, True)
        [0, 1, 2, 3, 4, 6, 7]
    """

    authorised_bids = list(range(n_cards + 1))
    if last_player:
        forbidden_bid = n_cards - total_bid

        if forbidden_bid >= 0:
            authorised_bids.remove(forbidden_bid)

    return authorised_bids


class GameEngine:

    """
    The main engine of the "oh hell" card game that manages the flow of the
    game.

    This class is responsible for orchestrating the game by handling players,
    distributing cards, playing rounds, and keeping track of the game state.

    :param point_attribution_strategy: The strategy used for attributing points
                                       to players.
    :type point_attribution_strategy: AbstractPointAttributionStrategy

    :Example:
        >>> game_engine = GameEngine()
        >>> player_1 = Player(1)
        >>> player_2 = Player(2)
        >>> game_engine.subscribe_player(player_1)
        >>> game_engine.subscribe_player(player_2)
        >>> points = game_engine.play_game(seed=42)
        {1: 35, 2: -76}
    """

    def __init__(
        self, point_attribution_strategy: AbstractPointAttributionStrategy
    ):

        Card.suit_ordered = True
        self._deck = Deck()
        self._players = list()

        self._point_attribution_strategy = point_attribution_strategy

        self._game_state = GameState()

    def subscribe_player(self, player: AbstractPlayer):

        """
        Subscribes a player to the game.

        :param player: The player to be added to the game.
        :type player: AbstractPlayer

        :Example:
            >>> game_engine = GameEngine()
            >>> player = Player(1)
            >>> game_engine.subscribe_player(player)
        """

        self._players.append(player)
        logging.info(f"Player {player.id} added")

    def unsubscribe_player(self, player: AbstractPlayer):

        """
        Unsubscribes a player from the game.

        :param player: The player to be removed from the game.
        :type player: AbstractPlayer

        :Example:
            >>> game_engine = GameEngine()
            >>> player = Player(1)
            >>> game_engine.subscribe_player(player)
            >>> game_engine.unsubscribe_player(player)
        """

        self._players = [p for p in self._players if p.id != player.id]
        logging.info(f"Player {player.id} removed")

    def notify_game_state(self):

        """
        Notifies all subscribed players about the current game state.
        """

        for player in self._players:
            player.update_game_state(self._game_state)

    def _distribute_cards(self, n_cards: int):

        """
        Distributes a specific number of cards to each player.

        :param n_cards: The number of cards to distribute to each player.
        :type n_cards: int
        """

        for _ in range(n_cards):
            for player in self._players:
                card = list(self._deck.draw())[0]
                player.add_to_hand(card)

    def _ordered_players(self, first_playerd_idx: int):

        """
        Orders the players based on the starting player index.

        :param first_playerd_idx: The index of the first player in this round.
        :type first_playerd_idx: int

        :return: The ordered list of players.
        :rtype: List[AbstractPlayer]
        """

        return (
            self._players[first_playerd_idx:] +
            self._players[:first_playerd_idx]
        )

    def play_game(self, seed: Optional[int] = None):

        """
        Plays the entire game, going through all the rounds.

        :param seed: The seed value for random operations, such as shuffling.
        :type seed: Optional[int]

        :return: The final points scored by each player.
        :rtype: Dict[int, int]

        :Example:
            >>> game_engine = GameEngine()
            >>> player_1 = Player(1)
            >>> player_2 = Player(2)
            >>> game_engine.subscribe_player(player_1)
            >>> game_engine.subscribe_player(player_2)
            >>> points = game_engine.play_game(seed=42)
            {1: 35, 2: -76}
        """

        players_idx = cycle(range(len(self._players)))
        max_n_cards = 51 // len(self._players)

        for round_idx in range(max_n_cards):

            self._deck.initialise(shuffle=True, seed=seed)
            first_player_idx = next(players_idx)
            self.play_round(round_idx, round_idx+1, first_player_idx)
            self._game_state.store_current_round()

        points_by_player_id = self._game_state.get_points_by_player_id()
        logging.info(f"Points: {points_by_player_id}")

        return points_by_player_id

    def play_round(self, round_id: int, n_cards: int, first_player_idx: int):

        """
        Plays a single round of the game.

        :param round_id: The identifier for the round.
        :type round_id: int
        :param n_cards: The number of cards to be played in this round.
        :type n_cards: int
        :param first_player_idx: The index of the first player in this round.
        :type first_player_idx: int

        :return: The points scored in this round by each player.
        :rtype: Dict[int, int]
        """

        logging.info(f"Round {round_id} | starting")
        logging.info(f"Round {round_id} | {n_cards} cards played")

        # distribute_card
        self._distribute_cards(n_cards)

        trump_card = list(self._deck.draw())[0]
        logging.info(f"Round {round_id} | trump card: {trump_card}")
        game_round = Round(
            round_id, trump_card, self._point_attribution_strategy
        )
        self._game_state.current_round = game_round
        self.notify_game_state()

        # make bids
        for i, player in enumerate(self._ordered_players(first_player_idx)):
            autorised_bids = get_authorised_bids(
                n_cards, game_round.total_bid, i+1 == len(self._players)
            )
            bid = player.make_bid(autorised_bids)
            game_round.add_bid(player.id, bid)
            self.notify_game_state()

        logging.info(
            f"Round {round_id} | bid round done ("
            f"{game_round.bid_by_player_id})"
        )
        logging.info(
            f"Round {round_id} | total bid: {game_round.total_bid}"
        )

        # play tricks
        for trick_idx in range(n_cards):

            self._play_trick(trick_idx, first_player_idx)

        self._game_state.store_current_round()

        round_points = game_round.get_points_by_player_id()
        logging.info(f"Round {round_id} | points: {round_points}")
        logging.info(f"Round {n_cards} | ending")

        return round_points

    def _play_trick(self, trick_id: int, first_player_idx: int):

        """
        Plays a single trick within a round.

        :param trick_id: The identifier for the trick.
        :type trick_id: int
        :param first_player_idx: The index of the first player in this trick.
        :type first_player_idx: int
        """

        logging.info(
            f"Round {self._game_state.current_round.id} | trick {trick_id} | "
            f"starting"
        )
        # play cards
        trick = Trick(trick_id)
        self._game_state.current_round.current_trick = trick
        for player in self._ordered_players(first_player_idx):

            authorised_cards = get_authorised_cards(player.hand, trick.suit)
            played_card = player.play_card(authorised_cards)
            trick.add_player_card(player.id, played_card)
            self.notify_game_state()
            logging.info(
                f"Round {self._game_state.current_round.id} | trick {trick_id}"
                f" | player {player.id} played {played_card}"
            )
        self._game_state.current_round.store_current_trick()

        logging.info(
            f"Round {self._game_state.current_round.id} | trick {trick_id} | "
            f"ending"
        )
