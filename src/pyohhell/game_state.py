#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Optional, Tuple, Dict

from pydecklib.card import Card, Suit, Value


class GameState:

    """
    Represents the state of a card game, tracking the progression of rounds.

    This class manages the rounds in a card game and calculates the cumulative
    points scored by each player across all rounds.

    :param rounds: A tuple of rounds played or to be played in the game.
    :type rounds: Tuple[Round, ...], optional

    :Example:
        >>> game_state = GameState()
        >>> _round.add_bid(player_id=1, bid=1)
        >>> _round.add_bid(player_id=2, bid=1)
        >>> _round = Round(1, Card(Suit.HEARTS, Value.ACE))
        >>> trick = Trick(
        ...     1,
        ...     (
        ...         (1, Card(Suit.SPADES, Value.TEN)),
        ...         (2, Card(Suit.SPADES, Value.JACK))
        ... ))
        >>> _round.current_trick = trick
        >>> _round.store_current_trick()
        >>> game_state.current_round = _round
        >>> game_state.store_current_round()
        >>> points = game_state.get_points_by_player_id()
        {1: -1, 2: 4}
    """

    def __init__(self, rounds: Tuple[Round, ...] = tuple()):

        self._rounds: List[Round] = list(rounds)
        self._current_round: Optional[Round] = None

    @property
    def current_round(self) -> Optional[Round]:

        """
        The current round being played in the game.

        :return: The current round, or None if no round is active.
        :rtype: Optional[Round]
        """

        return self._current_round

    @current_round.setter
    def current_round(self, value: Round):

        """
        Sets the current round of the game.

        :param value: The round to be set as current.
        :type value: Round
        """

        self._current_round = value

    def store_current_round(self) -> None:

        """
        Stores the current round in the game's round list and resets the
        current round.

        :Example:
            >>> game_state = GameState()
            >>> _round = Round(1, Card(Suit.HEARTS, Value.ACE))
            >>> game_state.current_round = _round
            >>> game_state.store_current_round()
            >>> game_state.current_round
            None
        """

        if self._current_round:
            self._rounds.append(self._current_round)
        self._current_round = None

    def get_points_by_player_id(self) -> Dict[int, int]:

        """
        Calculates the total points scored by each player across all rounds in
        the game.

        :return: A dictionary mapping player IDs to their total points.
        :rtype: defaultdict[int, int]

        :Example:
            >>> game_state = GameState()
            >>> _round.add_bid(player_id=1, bid=1)
            >>> _round.add_bid(player_id=2, bid=1)
            >>> _round = Round(1, Card(Suit.HEARTS, Value.ACE))
            >>> trick = Trick(
            ...     1,
            ...     (
            ...         (1, Card(Suit.SPADES, Value.TEN)),
            ...         (2, Card(Suit.SPADES, Value.JACK))
            ... ))
            >>> _round.current_trick = trick
            >>> _round.store_current_trick()
            >>> game_state.current_round = _round
            >>> game_state.store_current_round()
            >>> points = game_state.get_points_by_player_id()
            {1: -1, 2: 4}
        """

        total_points_by_player_id = defaultdict(int)
        for _round in self._rounds:
            round_points_by_player_id = _round.get_points_by_player_id()
            for player_id, points in round_points_by_player_id.items():
                total_points_by_player_id[player_id] += points

        return total_points_by_player_id

    def __eq__(self, other: GameState):

        return (
            self._rounds == other._rounds and
            self._current_round == other._current_round
        )


class AbstractPointAttributionStrategy(ABC):

    """
    Abstract class representing the point attribution strategy for a card game.

    This class provides a template for implementing different strategies to
    attribute points to players based on their wins and bids.
    """

    @abstractmethod
    def attribute_points(
        self, win_by_player_id: Dict[int, int],
        bid_by_player_id: Dict[int, int]
    ) -> Dict[int, int]:

        """
        Abstract method to be implemented for attributing points to players.

        :param win_by_player_id: A dictionary mapping player IDs to the number
                                 of tricks won.
        :type win_by_player_id: Dict[int, int]
        :param bid_by_player_id: A dictionary mapping player IDs to their bids.
        :type bid_by_player_id: Dict[int, int]

        :return: A dictionary mapping player IDs to their attributed points.
        :rtype: Dict[int, int]
        """

        pass


class DefaultPointAttributionStrategy(AbstractPointAttributionStrategy):

    """
    Default strategy for attributing points to players in a card game.

    This strategy awards points based on the accuracy of players' bids compared
    to their wins.
    """

    def attribute_points(
        self, win_by_player_id: Dict[int, int],
        bid_by_player_id: Dict[int, int]
    ) -> Dict[int, int]:

        """
        Attributes points to players based on their bids and wins.

        Players receive positive points if their number of wins matches their
        bid, and negative points based on the difference between wins and bids
        otherwise.

        :param win_by_player_id: A dictionary mapping player IDs to the number
                                 of tricks won.
        :type win_by_player_id: Dict[int, int]
        :param bid_by_player_id: A dictionary mapping player IDs to their bids.
        :type bid_by_player_id: Dict[int, int]

        :return: A dictionary mapping player IDs to their attributed points.
        :rtype: Dict[int, int]

        :raises ValueError: If the keys in `win_by_player_id` are not a subset
                            of the keys in `bid_by_player_id`.

        :Example:
        >>> strategy = DefaultPointAttributionStrategy()
        >>> win_by_player = {1: 3, 2: 2}
        >>> bid_by_player = {1: 3, 2: 4, 3: 1}
        >>> strategy.attribute_points(win_by_player, bid_by_player)
        {1: 6, 2: -2, 3: -1}
        """

        if set(win_by_player_id.keys()).issubset(set(bid_by_player_id.keys())):
            point_by_player_id = dict()
            for player_id, bid in bid_by_player_id.items():
                win = win_by_player_id.get(player_id, 0)
                if bid == win:
                    point_by_player_id[player_id] = 3 + bid
                else:
                    point_by_player_id[player_id] = -(abs(win-bid))

            return point_by_player_id

        else:
            raise ValueError(
                "`win_by_player_id` keys should be a subset of "
                "`bid_by_player_id` keys"
            )


class Round:

    """
    Represents a single round in a card game.

    A round consists of multiple tricks and manages the bidding and scoring for
    the round.

    :param _id: The unique identifier for the round.
    :type _id: int
    :param trump_card: The card that defines the trump suit for the round.
    :type trump_card: Card
    :param point_attribution_strategy: The strategy used for attributing points
                                       to players.
    :type point_attribution_strategy:
            Optional[AbstractPointAttributionStrategy]

    :Example:
        >>> _round = Round(1, Card(Suit.DIAMONDS, Value.TWO))
        >>> _round.add_bid(player_id=1, bid=1)
        >>> _round.add_bid(player_id=2, bid=1)
        >>> trick = Trick(
        ...     1,
        ...     (
        ...         (1, Card(Suit.SPADES, Value.TEN)),
        ...         (2, Card(Suit.DIAMONDS, Value.JACK))
        ... ))
        >>> _round.current_trick = trick
        >>> _round.store_current_trick()
        >>> _round.get_points_by_player_id()
        >>> {1: -1, 2: 4}
    """

    def __init__(
        self, _id: int, trump_card: Card,
        point_attribution_strategy: AbstractPointAttributionStrategy =
        DefaultPointAttributionStrategy()
    ):

        self._id = _id
        self._trump_card = trump_card
        self._tricks: List[Trick] = list()
        self._current_trick: Optional[Trick] = None

        self._bid_by_player_id = dict()
        self._point_attribution_strategy = point_attribution_strategy

    @property
    def id(self) -> int:

        """
        The unique identifier of the round.

        :return: The round's unique identifier.
        :rtype: int
        """

        return self._id

    @property
    def current_trick(self) -> Optional[Trick]:

        """
        The current trick being played in the round.

        :return: The current trick, or None if no trick is active.
        :rtype: Optional[Trick]
        """

        return self._current_trick

    @current_trick.setter
    def current_trick(self, value: Trick):

        """
        Sets the current trick of the round.

        :param value: The trick to be set as current.
        :type value: Trick
        """

        self._current_trick = value

    def store_current_trick(self) -> None:

        """
        Stores the current trick in the round's trick list and resets the
        current trick.

        :Example:
            >>> _round = Round(1, Card(Suit.DIAMONDS, Value.TWO))
            >>> trick = Trick(1)
            >>> _round.current_trick = trick
            >>> _round.store_current_trick()
            >>> _round.current_trick
            None
        """

        if self._current_trick:
            self._tricks.append(self._current_trick)
        self._current_trick = None

    @property
    def bid_by_player_id(self) -> Dict[int, int]:

        """
        Retrieves the bids made by players in the round.

        :return: Bids made by players.
        :rtype: Dict[int, int]
        """

        return self._bid_by_player_id

    @property
    def total_bid(self) -> int:

        """
        The total bid made by all players in the round.

        :return: The sum of all player bids.
        :rtype: int
        """

        return sum(self._bid_by_player_id.values())

    def add_bid(self, player_id: int, bid: int):

        """
        Adds a bid made by a player for the round.

        :param player_id: The ID of the player making the bid.
        :type player_id: int
        :param bid: The bid amount.
        :type bid: int

        :Example:
        >>> _round = Round(0)
        >>> _round.add_bid(player_id=1, bid=5)
        """

        if player_id is not None and bid is not None and \
                player_id not in self._bid_by_player_id:
            self._bid_by_player_id[player_id] = bid

    def get_wins_by_player_id(self):

        """
        Determines the number of tricks won by each player in the round.

        :return: A dictionary mapping player IDs to the number of tricks won.
        :rtype: defaultdict[int, int]
        """

        wins_by_player = defaultdict(int)
        for trick in self._tricks:
            winner_id, card = trick.get_winner(self._trump_card.suit)
            if winner_id:
                wins_by_player[winner_id] += 1

        return wins_by_player

    def get_points_by_player_id(self) -> Dict[int, int]:

        """
        Computes and returns the points scored by each player in the round.

        :return: A dictionary mapping player IDs to their scored points.
        :rtype: Dict[int, int]

    :Example:
        >>> _round = Round(1, Card(Suit.DIAMONDS, Value.TWO))
        >>> _round.add_bid(player_id=1, bid=1)
        >>> _round.add_bid(player_id=2, bid=1)
        >>> trick = Trick(
        ...     1,
        ...     (
        ...         (1, Card(Suit.SPADES, Value.TEN)),
        ...         (2, Card(Suit.DIAMONDS, Value.JACK))
        ... ))
        >>> _round.current_trick = trick
        >>> _round.store_current_trick()
        >>> _round.get_points_by_player_id()
        >>> {1: -1, 2: 4}
    """

        wins_by_player = self.get_wins_by_player_id()
        points_by_players = self._point_attribution_strategy.attribute_points(
            wins_by_player, self._bid_by_player_id
        )

        return points_by_players

    def __eq__(self, other):

        if not isinstance(other, Round):
            return False

        skipped_attrs = ['_point_attribution_strategy']

        for attr, value in vars(self).items():
            if getattr(other, attr, None) != value \
                    and attr not in skipped_attrs:
                return False
        return True


class Trick:

    """
    Represents a single trick in the card game.

    This class encapsulates the logic of managing a trick, which is a round
    in a card game where each player plays a card and the best card wins.

    :param _id: The unique identifier for the trick.
    :type _id: int
    :param player_ids_cards: A tuple of player ID and card pairs played in the
                             trick.
    :type player_ids_cards: Tuple[Tuple[int, Card], ...], optional

    :Example:
        >>> trick = Trick(
        ...     1,
        ...     (
        ...         (1, Card(Suit.SPADES, Value.TEN)),
        ...         (2, Card(Suit.SPADES, Value.JACK))
        ... ))
        >>> trick.add_player_card(3, Card(Suit.DIAMONDS, Value.FIVE))
        >>> trick.get_winner(Suit.DIAMONDS)
        >>> (3, 🃅)
    """

    def __init__(
        self, _id: int,
        player_ids_cards: Tuple[Tuple[int, Card], ...] = tuple()
    ):

        self._id = _id
        Card.suit_ordered = True
        self._player_ids_cards = list(player_ids_cards)

    @property
    def id(self) -> int:

        """
        The unique identifier of the trick.

        :return: The trick's unique identifier.
        :rtype: int
        """

        return self._id

    @property
    def suit(self) -> Optional[Suit]:

        """
        The suit of the trick which is the trick of the first card played in
        the trick.

        :return: The suit of the first card if any card is played, else None.
        :rtype: Optional[Suit]
        """

        if self._player_ids_cards:
            return self._player_ids_cards[0][1].suit
        else:
            return None

    def add_player_card(self, player_id: int, card: Card):

        """
        Adds a player's card to the trick.

        :param player_id: The ID of the player playing the card.
        :type player_id: int
        :param card: The card being played by the player.
        :type card: Card

        :Example:
            >>> trick = Trick(1)
            >>> trick.add_player_card(3, Card(Suit.DIAMONDS, Value.FIVE))
        """

        self._player_ids_cards.append((player_id, card))

    def get_winner(self, trump_suit: Suit) -> Tuple[
        Optional[int], Optional[Card]
    ]:

        """
        Determines the winner of the trick based on the trump suit and the
        played cards.

        :param trump_suit: The suit that trumps other suits in this trick.
        :type trump_suit: Suit

        :return: A tuple containing the winner's ID and its winning card.
        :rtype: Tuple[Optional[int], Optional[Card]]

        :raises ValueError: If the trick is empty.

    :Example:
        >>> trick = Trick(
        ...     1,
        ...     (
        ...         (1, Card(Suit.SPADES, Value.TEN)),
        ...         (2, Card(Suit.SPADES, Value.JACK))
        ... ))
        >>> trick.add_player_card(3, Card(Suit.DIAMONDS, Value.FIVE))
        >>> trick.get_winner(Suit.DIAMONDS)
        >>> (3, 🃅)
    """

        if self._player_ids_cards:

            cards = [card for player, card in self._player_ids_cards]
            suit_ranking = {
                suit: (
                    2 if suit == trump_suit
                    else 1 if suit == self.suit else 0
                )
                for suit in Suit
            }
            Card.suit_ranking = suit_ranking

            best_card = max(cards)
            best_card_idx = cards.index(best_card)

            return self._player_ids_cards[best_card_idx]

        else:
            return None, None

    def __eq__(self, other):
        if not isinstance(other, Trick):
            return False

        for attr, value in vars(self).items():
            if getattr(other, attr, None) != value:
                return False
        return True
