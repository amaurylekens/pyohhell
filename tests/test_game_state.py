#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydecklib.card import Card, Suit, Value
import pytest

from src.pyohhell.game_state import (
    DefaultPointAttributionStrategy,
    GameState,
    Round,
    Trick
)


# test trick_suit
test_values = [
    (tuple(), None),
    (((1, Card(Suit.SPADES, Value.TWO)), ), Suit.SPADES),
    (
        ((1, Card(Suit.SPADES, Value.TWO)), (2, Card(Suit.SPADES, Value.TWO))),
        Suit.SPADES
    )
]


@pytest.mark.parametrize('player_ids_cards, expected', test_values)
def test_trick_suit(player_ids_cards, expected):

    trick = Trick(0, player_ids_cards)
    actual = trick.suit
    assert actual == expected


# test trick_add_player_card
test_values = [
    (
        tuple(), 1, Card(Suit.SPADES, Value.TWO),
        [(1, Card(Suit.SPADES, Value.TWO))]
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
        ),
        2, Card(Suit.SPADES, Value.THREE),
        [
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.SPADES, Value.THREE))
        ]
    )
]


@pytest.mark.parametrize(
    'player_ids_cards, player_id, card, expected', test_values
)
def test_trick_add_player_card(player_ids_cards, player_id, card, expected):

    trick = Trick(0, player_ids_cards)
    trick.add_player_card(player_id, card)
    actual = trick._player_ids_cards
    assert actual == expected


# test trick_get_winner
test_values = [
    (tuple(), Suit.SPADES, (None, None)),
    (
        ((1, Card(Suit.SPADES, Value.TWO)), ), Suit.SPADES,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        ((1, Card(Suit.SPADES, Value.TWO)), ), Suit.DIAMONDS,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.SPADES, Value.THREE))
        ),
        Suit.SPADES,
        (2, Card(Suit.SPADES, Value.THREE))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.SPADES, Value.THREE))
        ),
        Suit.DIAMONDS,
        (2, Card(Suit.SPADES, Value.THREE))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.THREE))
        ),
        Suit.HEARTS,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO))
        ),
        Suit.SPADES,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO))
        ),
        Suit.DIAMONDS,
        (2, Card(Suit.DIAMONDS, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.ACE)),
            (2, Card(Suit.DIAMONDS, Value.TWO))
        ),
        Suit.DIAMONDS,
        (2, Card(Suit.DIAMONDS, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.DIAMONDS, Value.THREE))
        ),
        Suit.HEARTS,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.DIAMONDS, Value.THREE))
        ),
        Suit.SPADES,
        (1, Card(Suit.SPADES, Value.TWO))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.DIAMONDS, Value.THREE))
        ),
        Suit.DIAMONDS,
        (3, Card(Suit.DIAMONDS, Value.THREE))
    ),
    (
        (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.SPADES, Value.THREE))
        ),
        Suit.SPADES,
        (3, Card(Suit.SPADES, Value.THREE))
    )
]


@pytest.mark.parametrize(
    'players_ids_cards, trump_suit, expected', test_values
)
def test_trick_get_winner(players_ids_cards, trump_suit, expected):

    trick = Trick(0, players_ids_cards)
    actual = trick.get_winner(trump_suit)
    assert actual == expected


# test default_point_attribution_strategy_attribute_points
default_point_attribution_strategy = DefaultPointAttributionStrategy()
test_values = [
    (dict(), dict(), dict()),
    ({1: 1}, dict(), ValueError()),
    (dict(), {1: 1}, {1: -1}),
    ({1: 1}, {1: 1}, {1: 4}),
    ({1: 1}, {1: 0}, {1: -1}),
    ({1: 1}, {1: 3}, {1: -2}),
    ({1: 1, 2: 3}, {1: 1, 2: 2}, {1: 4, 2: -1})
]


@pytest.mark.parametrize(
    'win_by_player_id, bid_by_player_id, expected', test_values
)
def test_trick_default_point_attribution_strategy_attribute_points(
    win_by_player_id, bid_by_player_id, expected
):
    if isinstance(expected, Exception):
        with pytest.raises(type(expected)):
            default_point_attribution_strategy.attribute_points(
                win_by_player_id, bid_by_player_id
            )
    else:
        actual = default_point_attribution_strategy.attribute_points(
            win_by_player_id, bid_by_player_id
        )
        assert actual == expected


# Test Round

# test round_current_trick
test_values = [
    (None, None),
    (Trick(0), Trick(0)),
    (
        Trick(0, (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.SPADES, Value.THREE))
        )),
        Trick(0, (
            (1, Card(Suit.SPADES, Value.TWO)),
            (2, Card(Suit.DIAMONDS, Value.TWO)),
            (3, Card(Suit.SPADES, Value.THREE))
        ))
    )
]


@pytest.mark.parametrize(
    'trick, expected', test_values
)
def test_round_current_trick(trick, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    round._current_trick = trick
    actual = round.current_trick

    assert actual == expected


# test round_store_current_trick
test_values = [
    ([None], []),
    ([Trick(0)], [Trick(0)]),
    (
        [
            Trick(0, (
                (1, Card(Suit.SPADES, Value.TWO)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            )),
            Trick(1, (
                (1, Card(Suit.HEARTS, Value.TWO)),
                (2, Card(Suit.SPADES, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            ))
        ],
        [
            Trick(0, (
                (1, Card(Suit.SPADES, Value.TWO)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            )),
            Trick(1, (
                (1, Card(Suit.HEARTS, Value.TWO)),
                (2, Card(Suit.SPADES, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            ))
        ]
    )
]


@pytest.mark.parametrize(
    'tricks, expected', test_values
)
def test_round_store_current_trick(tricks, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    for trick in tricks:
        round._current_trick = trick
        round.store_current_trick()

    assert round.current_trick is None
    assert round._tricks == expected


# test round_total_bid
test_values = [
    (dict(), 0),
    ({1: 0}, 0),
    ({1: 2}, 2),
    ({1: 2, 2: 1}, 3)
]


@pytest.mark.parametrize('bid_by_player_id, expected', test_values)
def test_round_total_bid(bid_by_player_id, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    round._bid_by_player_id = bid_by_player_id
    actual = round.total_bid

    assert actual == expected


# test round_add_bid
test_values = [
    (dict(), None, None, dict()),
    (dict(), 1, None, dict()),
    (dict(), 1, 1, {1: 1}),
    ({1: 1}, 2, None, {1: 1}),
    ({1: 1}, 2, 3, {1: 1, 2: 3}),
    ({1: 1}, 1, 3, {1: 1})
]


@pytest.mark.parametrize(
    'bid_by_player_id, player_id, bid, expected', test_values
)
def test_round_add_bid(bid_by_player_id, player_id, bid, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    round._bid_by_player_id = bid_by_player_id
    round.add_bid(player_id, bid)
    actual = round._bid_by_player_id

    assert actual == expected


# test round_get_wins_by_player_id
test_values = [
    ([], dict()),
    (
        [
            Trick(0, (
                (1, Card(Suit.HEARTS, Value.FOUR)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            ))
        ],
        {3: 1}
    ),
    (
        [
            Trick(0, (
                (1, Card(Suit.HEARTS, Value.TWO)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            )),
            Trick(1, (
                (1, Card(Suit.DIAMONDS, Value.QUEEN)),
                (2, Card(Suit.DIAMONDS, Value.FOUR)),
                (3, Card(Suit.DIAMONDS, Value.JACK))
            ))
        ],
        {1: 1, 3: 1}
    )
]


@pytest.mark.parametrize('tricks, expected', test_values)
def test_round_get_wins_by_player_id(tricks, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    round._tricks = tricks
    actual = round.get_wins_by_player_id()

    assert actual == expected


# test round_get_points_by_player_id
test_values = [
    (dict(), [], dict()),
    (
        {1: 1, 2: 0, 3: 1},
        [
            Trick(0, (
                (1, Card(Suit.HEARTS, Value.FOUR)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            ))
        ],
        {1: -1, 2: 3, 3: 4}
    ),
    (
        {1: 0, 2: 0, 3: 1},
        [
            Trick(0, (
                (1, Card(Suit.HEARTS, Value.TWO)),
                (2, Card(Suit.DIAMONDS, Value.TWO)),
                (3, Card(Suit.SPADES, Value.THREE))
            )),
            Trick(1, (
                (1, Card(Suit.DIAMONDS, Value.QUEEN)),
                (2, Card(Suit.DIAMONDS, Value.FOUR)),
                (3, Card(Suit.DIAMONDS, Value.JACK))
            ))
        ],
        {1: -1, 2: 3, 3: 4}
    )
]


@pytest.mark.parametrize('bid_by_player, tricks, expected', test_values)
def test_round_get_points_by_player_id(bid_by_player, tricks, expected):

    round = Round(
        0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
    )

    round._bid_by_player_id = bid_by_player
    round._tricks = tricks
    actual = round.get_points_by_player_id()

    assert actual == expected


# test GameState

# test game_state_current_round
round_a = Round(
    0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
)
test_values = [
    (None, None),
    (round_a, round_a)
]


@pytest.mark.parametrize(
    'round, expected', test_values
)
def test_game_state_current_round(round, expected):

    game_state = GameState()

    game_state._current_round = round
    actual = game_state.current_round

    assert actual == expected


# test game_state_store_current_round

round_a = Round(
    0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
)
round_b = Round(
    1, Card(Suit.SPADES, Value.THREE), DefaultPointAttributionStrategy()
)

test_values = [
    ([None], []),
    ([round_a], [round_a]),
    ([round_a, None], [round_a]),
    ([round_a, round_b], [round_a, round_b])
]


@pytest.mark.parametrize(
    'rounds, expected', test_values
)
def test_game_state_store_current_round(rounds, expected):

    game_state = GameState()

    for round in rounds:
        game_state._current_round = round
        game_state.store_current_round()

    assert game_state.current_round is None
    assert game_state._rounds == expected


# test game_state_get_points_by_player_id
round_a = Round(
    0, Card(Suit.SPADES, Value.TWO), DefaultPointAttributionStrategy()
)
round_b = Round(
    0, Card(Suit.CLUBS, Value.TWO), DefaultPointAttributionStrategy()
)
trick_a = Trick(
    0,
    (
        (0, Card(Suit.SPADES, Value.TWO)),
        (1, Card(Suit.SPADES, Value.THREE)),
        (2, Card(Suit.SPADES, Value.FOUR))
    )
)
trick_b = Trick(
    0,
    (
        (0, Card(Suit.SPADES, Value.ACE)),
        (1, Card(Suit.DIAMONDS, Value.QUEEN)),
        (2, Card(Suit.HEARTS, Value.TEN))
    )
)
trick_c = Trick(
    1,
    (
        (0, Card(Suit.DIAMONDS, Value.ACE)),
        (1, Card(Suit.DIAMONDS, Value.TWO)),
        (2, Card(Suit.CLUBS, Value.TEN))
    )
)
round_a._tricks = [trick_a]
round_a._bid_by_player_id = {0: 1, 1: 1, 2: 1}
round_b._tricks = [trick_b, trick_a]
round_b._bid_by_player_id = {0: 1, 1: 1, 2: 1}
test_values = [
    ([round_a, round_b], {0: -2, 1: -2, 2: 8})
]


@pytest.mark.parametrize(
    'rounds, expected', test_values
)
def test_game_state_get_points_by_player_id(rounds, expected):

    game_state = GameState()
    game_state._rounds = rounds

    actual = game_state.get_points_by_player_id()

    assert actual == expected
