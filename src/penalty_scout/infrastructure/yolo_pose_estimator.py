import numpy as np
from ultralytics import YOLO

from penalty_scout.domain.pose import BodyPart, Keypoint, PersonPose


class YoloPoseEstimator:
    """PoseEstimator adapter backed by an Ultralytics YOLO pose model."""

    def __init__(self, model_name: str = "yolo11n-pose.pt") -> None:
        self._model = YOLO(model_name)

    def estimate(self, frame: np.ndarray) -> list[PersonPose]:
        result = self._model(frame, verbose=False)[0]
        if result.keypoints is None or result.keypoints.conf is None:
            return []

        coordinates = result.keypoints.xyn.cpu().numpy()  # (people, 17, 2), normalized
        confidences = result.keypoints.conf.cpu().numpy()  # (people, 17)

        return [
            PersonPose(
                {
                    part: Keypoint(float(x), float(y), float(conf))
                    for part, (x, y), conf in zip(BodyPart, person_xy, person_conf)
                }
            )
            for person_xy, person_conf in zip(coordinates, confidences)
        ]