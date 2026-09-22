import pytest

from penalty_scout.domain.shot_placement import Horizontal, ShotPlacement, Vertical


@pytest.mark.parametrize(
    "x, expected",
    [(0.1, Horizontal.LEFT), (0.5, Horizontal.CENTER), (0.9, Horizontal.RIGHT)],
)
def test_horizontal_zone(x, expected):
    assert ShotPlacement.from_goal_coordinates(x, 0.5).horizontal == expected


@pytest.mark.parametrize(
    "y, expected",
    [(0.1, Vertical.LOW), (0.5, Vertical.MIDDLE), (0.9, Vertical.HIGH)],
)
def test_vertical_zone(y, expected):
    assert ShotPlacement.from_goal_coordinates(0.5, y).vertical == expected


def test_ball_inside_goal_is_on_target():
    assert ShotPlacement.from_goal_coordinates(0.5, 0.5).on_target


@pytest.mark.parametrize(
    "x, y, horizontal, vertical",
    [
        (-0.2, 0.3, Horizontal.LEFT, Vertical.LOW),     # wide left
        (1.3, 0.5, Horizontal.RIGHT, Vertical.MIDDLE),  # wide right
        (0.5, 1.4, Horizontal.CENTER, Vertical.HIGH),   # over the bar
        (-0.1, 1.2, Horizontal.LEFT, Vertical.HIGH),    # over and wide left
    ],
)
def test_off_target_shot_keeps_its_side(x, y, horizontal, vertical):
    placement = ShotPlacement.from_goal_coordinates(x, y)
    assert not placement.on_target
    assert placement.horizontal == horizontal
    assert placement.vertical == vertical


def test_ball_below_ground_is_rejected():
    with pytest.raises(ValueError):
        ShotPlacement.from_goal_coordinates(0.5, -0.1)