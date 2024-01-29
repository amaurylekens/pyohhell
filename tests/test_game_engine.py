#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydecklib.card import Card, Suit, Value
import pytest

from src.pyohhell.game_state import DefaultPointAttributionStrategy
from src.pyohhell.player import Player
from src.pyohhell.game_state import (
    GameState,
    Round,
    Trick
)
from src.pyohhell.game_engine import (
    get_authorised_cards,
    get_authorised_bids,
    GameEngine
)


# test get_authorised_cards

test_values = [
    ([], Suit.SPADES, []),
    (
        [Card(Suit.SPADES, Value.TWO)], Suit.SPADES,
        [Card(Suit.SPADES, Value.TWO)]
    ),
    (
        [Card(Suit.DIAMONDS, Value.TWO)], Suit.SPADES,
        [Card(Suit.DIAMONDS, Value.TWO)]
    ),
    (
        [Card(Suit.DIAMONDS, Value.THREE), Card(Suit.DIAMONDS, Value.TWO)],
        Suit.SPADES,
        [Card(Suit.DIAMONDS, Value.THREE), Card(Suit.DIAMONDS, Value.TWO)]
    ),
    (
        [Card(Suit.SPADES, Value.THREE), Card(Suit.DIAMONDS, Value.TWO)],
        Suit.SPADES,
        [Card(Suit.SPADES, Value.THREE)]
    )
]


@pytest.mark.parametrize('cards, trick_suit, expected', test_values)
def test_get_authorised_cards(cards, trick_suit, expected):

    actual = get_authorised_cards(cards, trick_suit)
    assert actual == expected


# test get_authorised_bids

test_values = [
    (0, 0, False, [0]),
    (0, 0, True, []),
    (1, 0, False, [0, 1]),
    (1, 0, True, [0]),
    (1, 1, False, [0, 1]),
    (1, 1, True, [1]),
    (3, 1, False, [0, 1, 2, 3]),
    (3, 1, True, [0, 1, 3]),
]


@pytest.mark.parametrize(
    'n_cards, total_bid, last_player, expected', test_values
)
def test_get_authorised_bids(n_cards, total_bid, last_player, expected):

    actual = get_authorised_bids(n_cards, total_bid, last_player)
    assert actual == expected


# test GameEngine

# test game_engine_subscribe_player

ge_a = GameEngine(DefaultPointAttributionStrategy())
ge_b = GameEngine(DefaultPointAttributionStrategy())
player_a = Player(0)
ge_b._players = [player_a]

test_values = [
    (ge_a, player_a, ge_b),
    (ge_a, None, AttributeError())
]


@pytest.mark.parametrize('game_engine, player, expected', test_values)
def test_game_engine_subscribe_player(game_engine, player, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            game_engine.subscribe_player(player)
    else:
        game_engine.subscribe_player(player)
        actual = game_engine
        assert actual._players == expected._players


# test game_engine_unsubscribe_player

ge_a = GameEngine(DefaultPointAttributionStrategy())
ge_b = GameEngine(DefaultPointAttributionStrategy())
player_a = Player(0)
ge_b._players = [player_a]

test_values = [
    (ge_b, player_a, ge_a),
    (ge_a, None, AttributeError())
]


@pytest.mark.parametrize('game_engine, player, expected', test_values)
def test_game_engine_unsubscribe_player(game_engine, player, expected):

    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            game_engine.unsubscribe_player(player)
    else:
        game_engine.unsubscribe_player(player)
        actual = game_engine
        assert actual._players == expected._players


# test game_engine_notify_game_state

player_a_0 = Player(0)
player_a_1 = Player(1)

trick = Trick(
    0,
    (
        (player_a_0.id, Card(Suit.SPADES, Value.TWO)),
        (player_a_1.id, Card(Suit.SPADES, Value.THREE))
    )
)
game_round = Round(0, Card(Suit.HEARTS, Value.TWO))
game_state = GameState((game_round,))

player_b_0 = Player(0)
player_b_1 = Player(1)
player_b_0._game_state = game_state
player_b_1._game_state = game_state

test_values = [
    ([player_a_0, player_a_1], game_state, [player_b_0, player_b_1]),
]


@pytest.mark.parametrize('players, game_state, expected', test_values)
def test_game_notify_game_state(players, game_state, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    ge.subscribe_player(player_a_0)
    ge.subscribe_player(player_a_1)
    ge._game_state = game_state
    ge.notify_game_state()

    assert all(
        p1._game_state == p2._game_state
        for p1, p2 in zip(ge._players, expected)
    )


# test game_engine_distribute_cards

player_a_0 = Player(0)
player_a_1 = Player(1)

player_b_0 = Player(0)
player_b_0._hand = [Card(Suit.SPADES, Value.TWO)]
player_b_1 = Player(1)
player_b_1._hand = [Card(Suit.SPADES, Value.THREE)]

test_values = [
    ([player_a_0, player_a_1], [player_b_0, player_b_1]),
]


@pytest.mark.parametrize('players, expected', test_values)
def test_game_distribute_cards(players, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    for player in players:
        ge.subscribe_player(player)
    ge._distribute_cards(1)

    assert all(
        len(p1._hand) == len(p2._hand)
        for p1, p2 in zip(ge._players, expected)
    )


# test game_engine_ordered_players

player_0 = Player(0)
player_1 = Player(1)
player_2 = Player(2)

test_values = [
    ([player_0, player_1], 0, [player_0, player_1]),
    ([player_0, player_1], 1, [player_1, player_0]),
    ([player_0, player_1, player_2], 1, [player_1, player_2, player_0])
]


@pytest.mark.parametrize('players, first_playerd_idx, expected', test_values)
def test_game_ordered_players(players, first_playerd_idx, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    for player in players:
        ge.subscribe_player(player)

    actual = ge._ordered_players(first_playerd_idx)

    assert actual == expected


# test game_play_trick

player_a_0 = Player(0)
player_a_0._hand = [Card(Suit.SPADES, Value.TWO)]
player_a_1 = Player(1)
player_a_1._hand = [Card(Suit.SPADES, Value.THREE)]

trick_a = Trick(0)
trick_a._player_ids_cards = [
    (0, Card(Suit.SPADES, Value.TWO)), (1, Card(Suit.SPADES, Value.THREE))
]

test_values = [
    ([player_a_0, player_a_1], trick_a),
]


@pytest.mark.parametrize('players, expected', test_values)
def test_play_trick(players, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    ge._game_state._current_round = Round(0, Card(Suit.HEARTS, Value.QUEEN))
    for player in players:
        ge.subscribe_player(player)
    ge._play_trick(0, 0)

    actual = ge._game_state._current_round._tricks[0]

    assert actual == expected



# test game_play_round

player_a_0 = Player(0)
player_a_0._hand = [Card(Suit.SPADES, Value.TWO)]
player_a_1 = Player(1)
player_a_1._hand = [Card(Suit.SPADES, Value.THREE)]

trick_a = Trick(0)
trick_a._player_ids_cards = [
    (0, Card(Suit.SPADES, Value.TWO)), (1, Card(Suit.SPADES, Value.THREE))
]
round_a = Round(0, Card(Suit.DIAMONDS, Value.QUEEN))
round_a._bid_by_player_id = {0: 0, 1: 0}
round_a._tricks = [trick_a]

test_values = [
    ([player_a_0, player_a_1], 1, 0, round_a),
]


@pytest.mark.parametrize(
    'players, n_cards, first_player_idx, expected', test_values
)
def test_play_round(players, n_cards, first_player_idx, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    ge._deck.initialise(shuffle=True, seed=1)
    for player in players:
        ge.subscribe_player(player)
    ge.play_round(0, n_cards, first_player_idx)

    actual = ge._game_state._rounds[0]

    assert actual == expected


# test game_play_game

player_0 = Player(0)
player_1 = Player(1)
player_2 = Player(2)


test_values = [
    ([player_0, player_1], 1, {0: 75, 1: -193}),
    ([player_0, player_1, player_2], 1, {0: 51, 1: -30, 2: -51})
]


@pytest.mark.parametrize('players, seed, expected', test_values)
def test_play_game(players, seed, expected):

    ge = GameEngine(DefaultPointAttributionStrategy())
    for player in players:
        ge.subscribe_player(player)

    actual = ge.play_game(seed)

    assert actual == expected


