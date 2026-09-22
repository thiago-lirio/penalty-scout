from uuid import uuid4

import pytest

from penalty_scout.domain.penalty_kick import (
    InvalidPenaltyKickError,
    Outcome,
    PenaltyKick,
)
from penalty_scout.domain.shot_placement import Horizontal, ShotPlacement


def make_kick(x=0.1, y=0.5, dive=Horizontal.LEFT, outcome=Outcome.SAVED, **kwargs):
    """Test helper: builds a valid kick, overriding only what each test cares about."""
    return PenaltyKick(
        kicker="Kicker",
        goalkeeper="Keeper",
        placement=ShotPlacement.from_goal_coordinates(x, y),
        dive=dive,
        outcome=outcome,
        **kwargs,
    )


def test_valid_kick_is_created():
    kick = make_kick(dive=Horizontal.RIGHT, outcome=Outcome.GOAL)
    assert kick.outcome is Outcome.GOAL


@pytest.mark.parametrize("outcome", [Outcome.GOAL, Outcome.SAVED])
def test_goal_or_save_requires_shot_on_target(outcome):
    with pytest.raises(InvalidPenaltyKickError):
        make_kick(x=-0.2, outcome=outcome)


def test_off_target_kick_cannot_be_inside_goal():
    with pytest.raises(InvalidPenaltyKickError):
        make_kick(x=0.5, y=0.5, outcome=Outcome.OFF_TARGET)


@pytest.mark.parametrize("x", [0.0, -0.05])
def test_woodwork_can_be_measured_on_either_side_of_the_post(x):
    assert make_kick(x=x, outcome=Outcome.WOODWORK).outcome is Outcome.WOODWORK


def test_keeper_guessed_side_when_diving_to_shot_side():
    assert make_kick(x=0.1, dive=Horizontal.LEFT).keeper_guessed_side


def test_keeper_did_not_guess_side():
    kick = make_kick(x=0.1, dive=Horizontal.RIGHT, outcome=Outcome.GOAL)
    assert not kick.keeper_guessed_side


def test_kicks_with_same_data_are_different_entities():
    assert make_kick() != make_kick()


def test_kicks_with_same_id_are_the_same_entity():
    kick_id = uuid4()
    assert make_kick(kick_id=kick_id) == make_kick(kick_id=kick_id)