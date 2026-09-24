import cv2
import pytest
from ultralytics.utils import ASSETS

from penalty_scout.application.ports import PoseEstimator
from penalty_scout.domain.pose import BodyPart
from penalty_scout.infrastructure.yolo_pose_estimator import YoloPoseEstimator


@pytest.mark.integration
def test_yolo_finds_people_with_all_body_parts():
    estimator: PoseEstimator = YoloPoseEstimator()
    frame = cv2.imread(str(ASSETS / "zidane.jpg"))

    poses = estimator.estimate(frame)

    assert len(poses) >= 1
    assert set(poses[0].keypoints) == set(BodyPart)