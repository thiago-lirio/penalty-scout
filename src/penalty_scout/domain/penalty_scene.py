from dataclasses import dataclass
from collections.abc import Iterable

from penalty_scout.domain.pose import BodyPart, PersonPose

HIPS = (BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP)


class SceneNotRecognizedError(ValueError):
    """Raised when a frame does not show a recognizable penalty scene."""


def _hip_height(pose: PersonPose) -> float | None:
    """Average vertical position of the visible hips, or None if none are visible."""
    heights = [hip.y for part in HIPS if (hip := pose.visible(part)) is not None]
    if not heights:
        return None
    return sum(heights) / len(heights)


@dataclass(frozen=True)
class PenaltyScene:
    """The two people that matter in a penalty, seen from behind the kicker."""

    kicker: PersonPose
    goalkeeper: PersonPose

    @classmethod
    def from_poses(cls, poses: Iterable[PersonPose]) -> "PenaltyScene":
        located = [(height, pose) for pose in poses if (height := _hip_height(pose)) is not None]
        if len(located) < 2:
            raise SceneNotRecognizedError(
                f"A penalty scene needs at least 2 people with visible hips, found {len(located)}"
            )

        located.sort(key=lambda pair: pair[0])
        return cls(kicker=located[-1][1], goalkeeper=located[0][1])