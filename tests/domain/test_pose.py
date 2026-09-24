import pytest

from penalty_scout.domain.pose import BodyPart, Keypoint, PersonPose


def make_pose(confidence):
    return PersonPose({part: Keypoint(0.5, 0.5, confidence) for part in BodyPart})


def test_keypoint_confidence_must_be_between_0_and_1():
    with pytest.raises(ValueError):
        Keypoint(0.5, 0.5, confidence=1.5)


def test_body_parts_follow_coco_model_order():
    parts = list(BodyPart)
    assert len(parts) == 17
    assert parts[0] is BodyPart.NOSE
    assert parts[15] is BodyPart.LEFT_ANKLE


def test_confident_keypoint_is_visible():
    assert make_pose(0.9).visible(BodyPart.LEFT_ANKLE) is not None


def test_low_confidence_keypoint_is_not_visible():
    assert make_pose(0.2).visible(BodyPart.LEFT_ANKLE) is None