#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydecklib.card import Card, Suit, Value
import pytest

from src.pyohhell.game_state import GameState, Round
from src.pyohhell.player import (
    RandomCardSelectionStrategy,
    FirstCardSelectionStrategy,
    RandomBidSelectionStrategy,
    FirstBidSelectionStrategy,
    Player
)

# test player_id
test_values = [
    (1, 1), (2, 2)
]


@pytest.mark.parametrize('_id, expected', test_values)
def test_player_id(_id, expected):

    p = Player(_id)
    actual = p.id
    assert actual == expected


# test player_hand
test_values = [
    (tuple(), []),
    ((Card(Suit.SPADES, Value.TWO),), [Card(Suit.SPADES, Value.TWO)]),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.DIAMONDS, Value.TWO)),
        [Card(Suit.SPADES, Value.TWO), Card(Suit.DIAMONDS, Value.TWO)]
    )
]


@pytest.mark.parametrize('hand, expected', test_values)
def test_player_hand(hand, expected):

    p = Player(1, initial_hand=hand)
    actual = p.hand
    assert actual == expected


# test player_add_to_hand
test_values = [
    (tuple(), Card(Suit.SPADES, Value.TWO), [Card(Suit.SPADES, Value.TWO)]),
    (
        (Card(Suit.SPADES, Value.TWO),),
        Card(Suit.SPADES, Value.THREE),
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)]
    )
]


@pytest.mark.parametrize('initial_hand, card, expected', test_values)
def test_player_add_to_hand(initial_hand, card, expected):

    p = Player(1, initial_hand=initial_hand)
    p.add_to_hand(card)
    actual = p.hand
    assert actual == expected


# test player_update_game_state
test_values = [
    (GameState(), GameState()),
    (
        GameState((Round(0, Card(Suit.SPADES, Value.TWO)),)),
        GameState((Round(0, Card(Suit.SPADES, Value.TWO)),))
    ),
    (
        GameState((
            Round(0, Card(Suit.SPADES, Value.TWO)),
            Round(1, Card(Suit.SPADES, Value.THREE))
        )),
        GameState((
            Round(0, Card(Suit.SPADES, Value.TWO)),
            Round(1, Card(Suit.SPADES, Value.THREE))
        ))
    )
]


@pytest.mark.parametrize('game_state, expected', test_values)
def test_player_update_game_state(game_state, expected):

    p = Player(1)
    p.update_game_state(game_state)
    actual = p._game_state
    assert actual == expected


# test player_play_card
test_values = [
    (tuple(), [], ValueError()),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)),
        [],
        ValueError()
    ),
    (
        tuple(),
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        ValueError()
    ),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)),
        [Card(Suit.SPADES, Value.FOUR), Card(Suit.SPADES, Value.FIVE)],
        ValueError()
    ),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)),
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.FOUR)],
        ValueError()
    ),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)),
        [Card(Suit.SPADES, Value.TWO)],
        Card(Suit.SPADES, Value.TWO)
    ),
    (
        (Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)),
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        Card(Suit.SPADES, Value.TWO)
    )
]


@pytest.mark.parametrize(
    'initial_hand, authorised_cards, expected', test_values
)
def test_play_card(initial_hand, authorised_cards, expected):

    p = Player(1, initial_hand=initial_hand)

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            p.play_card(authorised_cards)

    else:
        actual = p.play_card(authorised_cards)
        assert actual == expected


# test player_make_bid
test_values = [
    ([], ValueError()),
    ([1], 1), ([1, 2], 1)
]


@pytest.mark.parametrize('authorised_bids, expected', test_values)
def test_player_make_bid(authorised_bids, expected):

    p = Player(1)

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            p.make_bid(authorised_bids)

    else:
        actual = p.make_bid(authorised_bids)
        assert actual == expected


# test player__eq__
test_values = [
    (Player(1), 'player', TypeError()),
    (Player(1), Player(1), True), (Player(1), Player(2), False)
]


@pytest.mark.parametrize(
    'player, other, expected', test_values
)
def test_player__eq__(player, other, expected):

    p = Player(1)

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            player.__eq__(other)

    else:
        actual = player.__eq__(other)
        assert actual == expected


# test player__str__
test_values = [
    (Player(1), "Player_1")
]


@pytest.mark.parametrize('player, expected', test_values)
def test_player__str__(player, expected):

    p = Player(1)
    actual = p.__str__()
    assert actual == expected


# test random_card_selection_strategy_select_card

random_card_selection_strategy = RandomCardSelectionStrategy(seed=42)
test_values = [
    (
        [Card(Suit.SPADES, Value.TWO)], [],
        GameState(), None
    ),
    (
        [Card(Suit.SPADES, Value.TWO)], [Card(Suit.SPADES, Value.TWO)],
        GameState(), Card(Suit.SPADES, Value.TWO)
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [Card(Suit.SPADES, Value.TWO)],
        GameState(), Card(Suit.SPADES, Value.TWO)
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE), ],
        GameState(), Card(Suit.SPADES, Value.TWO)
    )
]


@pytest.mark.parametrize(
    'hand, authorised_cards, game_state, expected', test_values
)
def test_random_card_selection_strategy_select_card(
    hand, authorised_cards, game_state, expected
):

    actual = random_card_selection_strategy.select_card(
        hand, authorised_cards, game_state
    )
    assert actual == expected


# test first_card_selection_strategy_select_card

first_card_selection_strategy = FirstCardSelectionStrategy()
test_values = [
    (
        [Card(Suit.SPADES, Value.TWO)], [],
        GameState(), None
    ),
    (
        [Card(Suit.SPADES, Value.TWO)], [Card(Suit.SPADES, Value.TWO)],
        GameState(), Card(Suit.SPADES, Value.TWO)
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [Card(Suit.SPADES, Value.TWO)],
        GameState(), Card(Suit.SPADES, Value.TWO)
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE), ],
        GameState(), Card(Suit.SPADES, Value.TWO)
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [Card(Suit.SPADES, Value.THREE), Card(Suit.SPADES, Value.TWO), ],
        GameState(), Card(Suit.SPADES, Value.THREE)
    )
]


@pytest.mark.parametrize(
    'hand, authorised_cards, game_state, expected', test_values
)
def test_first_card_selection_strategy_select_card(
        hand, authorised_cards, game_state, expected
):

    actual = first_card_selection_strategy.select_card(
        hand, authorised_cards, game_state
    )
    assert actual == expected


# test random_bid_selection_strategy_select_bid

random_bid_selection_strategy = RandomBidSelectionStrategy(seed=42)
test_values = [
    ([Card(Suit.SPADES, Value.TWO)], [], GameState(), None),
    ([Card(Suit.SPADES, Value.TWO)], [1], GameState(), 1),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [1], GameState(), 1
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [1, 2], GameState(), 1
    )
]


@pytest.mark.parametrize(
    'hand, authorised_bids, game_state, expected', test_values
)
def test_random_bid_selection_strategy_select_card(
    hand, authorised_bids, game_state, expected
):

    actual = random_bid_selection_strategy.select_bid(
        hand, authorised_bids, game_state
    )
    assert actual == expected


# test first_bid_selection_strategy_select_bid

first_bid_selection_strategy = FirstBidSelectionStrategy()
test_values = [
    ([Card(Suit.SPADES, Value.TWO)], [], GameState(), None),
    ([Card(Suit.SPADES, Value.TWO)], [1], GameState(), 1),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [1], GameState(), 1
    ),
    (
        [Card(Suit.SPADES, Value.TWO), Card(Suit.SPADES, Value.THREE)],
        [1, 2], GameState(), 1
    )
]


@pytest.mark.parametrize(
    'hand, authorised_bids, game_state, expected', test_values
)
def test_first_bid_selection_strategy_select_card(
    hand, authorised_bids, game_state, expected
):

    actual = first_bid_selection_strategy.select_bid(
        hand, authorised_bids, game_state
    )
    assert actual == expected



