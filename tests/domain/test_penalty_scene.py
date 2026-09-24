import pytest

from penalty_scout.domain.pose import BodyPart, Keypoint, PersonPose
from penalty_scout.domain.penalty_scene import PenaltyScene, SceneNotRecognizedError

def pose_at(y: float, hip_confidence: float = 0.9) -> PersonPose:
  """A pose whose hips sit at height y (0 = top of the image, 1 = bottom)."""
  keypoints = {part: Keypoint(0.5, y, 0.9) for part in BodyPart}
  for hip in (BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP):
    keypoints[hip] = Keypoint(0.5, y, hip_confidence)
  return PersonPose(keypoints)

def test_kicker_is_the_closest_person_to_the_camera():
  keeper, referee, kicker = pose_at(0.2), pose_at(0.5), pose_at(0.9)

  scene = PenaltyScene.from_poses([keeper, referee, kicker])

  assert scene.kicker is kicker
  assert scene.goalkeeper is keeper

def test_poses_without_visible_hips_are_ignored():
    keeper, kicker = pose_at(0.2), pose_at(0.8)
    noise = pose_at(0.95, hip_confidence=0.1)

    scene = PenaltyScene.from_poses([keeper, noise, kicker])

    assert scene.kicker is kicker

@pytest.mark.parametrize(
    "poses",
    [
        [],
        [pose_at(0.5)],
        [pose_at(0.2), pose_at(0.9, hip_confidence=0.1)],
    ],
    ids=["no one", "only one person", "only one with visible hips"],
)
def test_scene_needs_at_least_two_people(poses):
    with pytest.raises(SceneNotRecognizedError):
        PenaltyScene.from_poses(poses)