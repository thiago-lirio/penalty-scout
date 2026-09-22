from dataclasses import dataclass
from enum import Enum

LOWER_THIRD_LIMIT = 1 / 3
UPPER_THIRD_LIMIT = 2 / 3


class Horizontal(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Vertical(Enum):
    LOW = "low"
    MIDDLE = "middle"
    HIGH = "high"


def _third(value: float) -> int:
    """Return 0, 1 or 2 depending on which third of the goal the value falls in."""
    if value < LOWER_THIRD_LIMIT:
        return 0
    if value > UPPER_THIRD_LIMIT:
        return 2
    return 1


@dataclass(frozen=True)
class ShotPlacement:
    """Where the ball crossed the goal line, from the kicker's point of view.

    Coordinates are normalized: x=0 is the kicker's left post, x=1 the right post,
    y=0 the ground and y=1 the crossbar. Values outside 0-1 mean the shot missed.
    """

    horizontal: Horizontal
    vertical: Vertical
    on_target: bool

    @classmethod
    def from_goal_coordinates(cls, x: float, y: float) -> "ShotPlacement":
        if y < 0:
            raise ValueError(f"Ball cannot be below the ground, got y={y}")

        on_target = 0 <= x <= 1 and 0 <= y <= 1
        horizontal = list(Horizontal)[_third(x)]
        vertical = list(Vertical)[_third(y)]
        return cls(horizontal, vertical, on_target)