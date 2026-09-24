from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

DEFAULT_MIN_CONFIDENCE = 0.5


class BodyPart(Enum):
    """COCO keypoints, in the exact order pose models output them.
    Sides are anatomical (the person's own left), NOT the goal sides."""

    NOSE = 0
    LEFT_EYE = 1
    RIGHT_EYE = 2
    LEFT_EAR = 3
    RIGHT_EAR = 4
    LEFT_SHOULDER = 5
    RIGHT_SHOULDER = 6
    LEFT_ELBOW = 7
    RIGHT_ELBOW = 8
    LEFT_WRIST = 9
    RIGHT_WRIST = 10
    LEFT_HIP = 11
    RIGHT_HIP = 12
    LEFT_KNEE = 13
    RIGHT_KNEE = 14
    LEFT_ANKLE = 15
    RIGHT_ANKLE = 16


@dataclass(frozen=True)
class Keypoint:
    """A body point in image coordinates normalized to 0-1 (x to the right, y downward)."""

    x: float
    y: float
    confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")


@dataclass(frozen=True)
class PersonPose:
    keypoints: Mapping[BodyPart, Keypoint]

    def visible(
        self, part: BodyPart, min_confidence: float = DEFAULT_MIN_CONFIDENCE
    ) -> Keypoint | None:
        keypoint = self.keypoints.get(part)
        if keypoint is None or keypoint.confidence < min_confidence:
            return None
        return keypoint