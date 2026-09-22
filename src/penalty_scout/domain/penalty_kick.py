from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from penalty_scout.domain.shot_placement import Horizontal, ShotPlacement


class Outcome(Enum):
    GOAL = "goal"
    SAVED = "saved"
    WOODWORK = "woodwork"
    OFF_TARGET = "off_target"


class InvalidPenaltyKickError(ValueError):
    """Raised when a penalty kick breaks a domain rule."""

@dataclass(eq=False)
class PenaltyKick:
    """A single penalty kick. Sides are always from the kicker's point of view,
    including the goalkeeper's dive."""

    kicker: str
    goalkeeper: str
    placement: ShotPlacement
    dive: Horizontal
    outcome: Outcome
    kick_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        requires_on_target = self.outcome in (Outcome.GOAL, Outcome.SAVED)
        if requires_on_target and not self.placement.on_target:
            raise InvalidPenaltyKickError(
                f"A kick with outcome '{self.outcome.value}' must be on target"
            )
        if self.outcome is Outcome.OFF_TARGET and self.placement.on_target:
            raise InvalidPenaltyKickError("An off-target kick cannot be inside the goal")

    @property
    def keeper_guessed_side(self) -> bool:
        return self.dive == self.placement.horizontal

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PenaltyKick):
            return NotImplemented
        return self.kick_id == other.kick_id

    def __hash__(self) -> int:
        return hash(self.kick_id)