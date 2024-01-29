#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List, Tuple, Optional
from abc import abstractmethod, ABC
import random

from pydecklib.card import Card

from src.pyohhell.game_state import GameState


class AbstractCardSelectionStrategy:

    """
    Abstract class that defines the structure for card selection strategy  in
    a card game.
    """

    @abstractmethod
    def select_card(
        self, hand: List[Card], authorised_cards: List[Card],
        game_state: GameState
    ) -> Optional[Card]:

        """
        Abstract method to select a card in a card game.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_cards: Cards that are allowed to be played based on
                                 the game rules.
        :type authorised_cards: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        pass


class RandomCardSelectionStrategy(AbstractCardSelectionStrategy):

    """
    Strategy for selecting a card randomly from the authorised cards.
    """

    def __init__(self, seed: Optional[int] = None):

        """
        :param seed: Seed for the random number generator.
        :type seed: Optional[int]
        """

        self._seed = seed

    def select_card(
        self, hand: List[Card], authorised_cards: List[Card],
        game_state: GameState
    ) -> Optional[Card]:

        """
        Method to randomly select a card from the authorised cards.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_cards: Cards that are allowed to be played based on
                                 the game rules.
        :type authorised_cards: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        if authorised_cards:
            if self._seed:
                random.seed(self._seed)
            return random.choice(authorised_cards)
        else:
            return None


class FirstCardSelectionStrategy(AbstractCardSelectionStrategy):

    """
    Strategy for selecting the first card from the authorised cards.
    """

    def select_card(
        self, hand: List[Card], authorised_cards: List[Card],
        game_state: GameState
    ) -> Optional[Card]:

        """
        Method to select the first card from the authorised cards.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_cards: Cards that are allowed to be played based on
                                 the game rules.
        :type authorised_cards: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        if authorised_cards:
            return authorised_cards[0]
        else:
            return None


class AbstractBidSelectionStrategy:

    """
    Abstract class that defines the structure for bid selection strategy in
    a card game.
    """

    @abstractmethod
    def select_bid(
        self, hand: List[Card], authorised_bids: List[int],
        game_state: GameState
    ) -> Optional[int]:

        """
        Abstract method to select a bid in a card game.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_bids: Bids that are allowed to be played based on
                                the game rules.
        :type authorised_bids: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        pass


class RandomBidSelectionStrategy(AbstractBidSelectionStrategy):

    """
    Strategy for selecting a card randomly from the authorised cards.
    """

    def __init__(self, seed: Optional[int] = None):

        """
        :param seed: Seed for the random number generator.
        :type seed: Optional[int]
        """

        self._seed = seed

    def select_bid(
        self, hand: List[Card], authorised_bids: List[int],
        game_state: GameState
    ) -> Optional[int]:

        """
        Method to randomly select a bid from the authorised bids.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_bids: Cards that are allowed to be played based on
                                 the game rules.
        :type authorised_bids: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        if authorised_bids:
            if self._seed:
                random.seed(self._seed)
            return random.choice(authorised_bids)
        else:
            return None


class FirstBidSelectionStrategy(AbstractBidSelectionStrategy):

    """
    Strategy for selecting the first bid from the authorised cards.
    """

    def select_bid(
        self, hand: List[Card], authorised_bids: List[int],
        game_state: GameState
    ) -> Optional[int]:

        """
        Method to select the first bid from the authorised bids.

        :param hand: The current hand of the player.
        :type hand: List[Card]
        :param authorised_bids: Cards that are allowed to be played based on
                                 the game rules.
        :type authorised_bids: List[Card]
        :param game_state: The current state of the game.
        :type game_state: GameState
        :return: The selected card or None if no card can be selected.
        :rtype: Optional[Card]
        """

        if authorised_bids:
            return authorised_bids[0]
        else:
            return None


class AbstractPlayer(ABC):

    """
    Abstract base class representing a 'oh hell' player in a card game. This
    class defines the basic properties and methods that all player subclasses
    should implement.

    Properties:
        id: Unique identifier for the player.
        hand: Current set of cards held by the player.
    """

    @property
    @abstractmethod
    def id(self) -> int:

        """
        Property representing the player's unique identifier.

        :return: The unique identifier of the player.
        :rtype: int
        """

        pass

    @property
    @abstractmethod
    def hand(self) -> List[Card]:

        """
        Property representing the current hand of the player.

        :return: The current set of cards held by the player.
        :rtype: List[Card]
        """

        pass

    @abstractmethod
    def update_game_state(self, game_state: GameState):

        """
        Update the player's knowledge of the game state.

        :param game_state: The current state of the game.
        :type game_state: GameState
        """

        pass

    @abstractmethod
    def play_card(self, authorised_cards: List[Card]) -> Card:

        """
        Determine and return a card to be played from the player's hand.

        :param authorised_cards: List of cards that the player is allowed
                                 to play.
        :type authorised_cards: List[Card]
        :return: The card chosen to be played.
        :rtype: Card
        """

        pass

    @abstractmethod
    def make_bid(self, authorised_bids: List[int]) -> int:

        """
        Make a bid on the won tricks based on the game rules and the player's
        strategy.

        :param authorised_bids: List of bids that the player is allowed to
                                make.
        :type authorised_bids: List[int]
        :return: The bid chosen by the player.
        :rtype: int
        """

        pass


class Player(AbstractPlayer):

    """
    A concrete implementation of AbstractPlayer that represents a player in the
    game.

    This class manages the player's hand, game state, and use costomisable
    strategies for card selection and bidding.
    """

    def __init__(
        self, _id: int,
        card_selection_strategy: AbstractCardSelectionStrategy =
        FirstCardSelectionStrategy(),
        bid_selection_strategy: AbstractBidSelectionStrategy =
        FirstBidSelectionStrategy(),
        initial_hand: Tuple[Card] = tuple()
    ):

        """
        :param _id: Unique identifier for the player.
        :type _id: int
        :param card_selection_strategy: Strategy used to select a card to play.
        :type card_selection_strategy: AbstractCardSelectionStrategy
        :param bid_selection_strategy: Strategy used to make a bid.
        :type bid_selection_strategy: AbstractBidSelectionStrategy
        :param initial_hand: Initial set of cards for the player's hand.
        :type initial_hand: Tuple[Card]
        """
        self._id: int = _id

        self._hand: List[Card] = list(initial_hand)
        self._card_selection_strategy: AbstractCardSelectionStrategy = \
            card_selection_strategy
        self._bid_selection_strategy: AbstractBidSelectionStrategy = \
            bid_selection_strategy

        self._game_state = GameState()

    @property
    def id(self) -> int:

        """
        Property representing the player's unique identifier.

        :return: The unique identifier of the player.
        :rtype: int
        """

        return self._id

    @property
    def hand(self) -> List[Card]:

        """
        Property representing the current hand of the player.

        :return: The current set of cards held by the player.
        :rtype: List[Card]
        """

        return self._hand

    def add_to_hand(self, card):

        """
        Add a card to the player's hand.

        :param card: The card to add.
        :type card: Card
        """

        self._hand.append(card)

    def update_game_state(self, game_state):

        """
        Update the player's knowledge of the game state.

        :param game_state: The current state of the game.
        :type game_state: GameState
        """

        self._game_state = game_state

    def play_card(self, authorised_cards: List[Card]) -> Card:

        """
        Determine and return the card to be played from the player's hand
        following the configured strategy.
        Raises an exception if authorised cards are not in the player's hand or
        if the list is empty.

        :param authorised_cards: List of cards that the player is allowed to
                                 play.
        :type authorised_cards: List[Card]
        :return: The card chosen to be played.
        :rtype: Optional[Card]
        :raises ValueError: If `authorised_cards` contains cards not in the
                            player's hand or is empty.
        """

        if authorised_cards:

            if all(card in self._hand for card in authorised_cards):

                played_card = self._card_selection_strategy.select_card(
                    self._hand, authorised_cards, self._game_state
                )
                self._hand.remove(played_card)

                return played_card

            else:
                raise ValueError(
                    "`autorised_cards` should contain only cards of `hand`"
                )

        else:
            raise ValueError("`autorised_cards` shouldn't be empty")

    def make_bid(self, authorised_bids: List[int]) -> int:

        """
        Make a bid based on the game rules and the configured strategy.
        Raises an exception if the list of authorised bids is empty.

        :param authorised_bids: List of bids that the player is allowed to
                                make.
        :type authorised_bids: List[int]
        :return: The bid chosen by the player.
        :rtype: int
        :raises ValueError: If `authorised_bids` is empty.
        """

        if authorised_bids:
            trick_bet = self._bid_selection_strategy.select_bid(
                self._hand, authorised_bids, self._game_state
            )

            return trick_bet

        else:
            raise ValueError("`autorised_bids` shouldn't be empty")

    def __eq__(self, other: Player):

        if isinstance(other, Player):
            return self._id == other._id

        else:
            raise TypeError(f"Can't compare Player to {type(other)}")

    def __str__(self):

        return f"Player_{self._id}"
