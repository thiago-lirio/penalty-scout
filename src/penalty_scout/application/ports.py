from typing import Protocol

import numpy as np

from penalty_scout.domain.pose import PersonPose


class PoseEstimator(Protocol):
    """Anything that can find people and their body keypoints in a video frame."""

    def estimate(self, frame: np.ndarray) -> list[PersonPose]: ...