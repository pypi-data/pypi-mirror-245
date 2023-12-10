import pytest
import numpy as np
from ekf_slam import KnownCorrespondence

@pytest.fixture
def known_correspondence():
    init = np.array([0, 0, 0])
    num_landmarks = 10

    # sensor model noise parameters
    Qt = np.array([[0.1, 0], [0, 0.05]])

    # movement model noise parameters
    Rt = 0.05 * np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    return KnownCorrespondence(init, num_landmarks, Qt, Rt)

def test_unobserved_landmark(known_correspondence: KnownCorrespondence):
    assert known_correspondence.landmark_pos(0) is None

@pytest.mark.parametrize("dist,angle,expected_x,expected_y", [
    (1, 0, 1, 0),
    (1, np.pi / 2, 0, 1),
    (1, np.pi, -1, 0),
    (1, 3 * np.pi / 2, 0, -1),
])
def test_predict(dist, angle, expected_x, expected_y, known_correspondence: KnownCorrespondence):
    known_correspondence.predict(np.array([dist, angle]))
    assert np.allclose(known_correspondence.robot_pos(), np.array([expected_x, expected_y]))

def test_update(known_correspondence: KnownCorrespondence):
    landmarks = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1],
    ]
    xy_movements = [
        (1, 1),
        (0.5, -1),
        (-0.5, -0.5)
    ]

    def sensor_readings(x, y):
        readings = []
        for i in range(len(landmarks)):
            dx = landmarks[i][0] - x
            dy = landmarks[i][1] - y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            angle = np.arctan2(dy, dx)
            readings.append([distance, angle, i])
        return readings

    prev_x, prev_y = known_correspondence.mean[:2]
    for x, y in xy_movements:
        dist = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
        angle = np.arctan2(y - prev_y, x - prev_x)

        known_correspondence.predict(np.array([dist, angle]))
        known_correspondence.update(np.array(sensor_readings(x, y)))

        ekf_slam_landmark_pos = []
        for i in range(known_correspondence.num_landmarks):
            landmark_pos = known_correspondence.landmark_pos(i)
            if landmark_pos is not None:
                ekf_slam_landmark_pos.append(landmark_pos[0])
                ekf_slam_landmark_pos.append(landmark_pos[1])

        # we don't care about the heading
        assert np.allclose(known_correspondence.robot_pos(), np.array([x, y]))
        assert np.allclose(np.array([known_correspondence.landmark_pos(i) for i in range(4)]), np.array(landmarks), atol=0.2)
        prev_x, prev_y = x, y


def test_update_noise(known_correspondence: KnownCorrespondence):
    landmarks = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1],
    ]
    xy_movements = [
        (1, 1),
        (0.5, -1),
        (-0.5, -0.5)
    ]

    def sensor_readings(x, y):
        readings = []
        for i in range(len(landmarks)):
            dx = landmarks[i][0] - x
            dy = landmarks[i][1] - y
            distance = np.sqrt(dx ** 2 + dy ** 2)
            angle = np.arctan2(dy, dx) + np.random.randn() * 0.05
            readings.append([distance, angle, i])
        return readings

    # boost a few times to reduce randomness impact
    for _ in range(3):
        try:
            prev_x, prev_y = known_correspondence.mean[:2]
            for x, y in xy_movements:
                dist = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
                angle = np.arctan2(y - prev_y, x - prev_x) + np.random.randn() * 0.05

                known_correspondence.predict(np.array([dist, angle]))
                known_correspondence.update(np.array(sensor_readings(x, y)))

                # we don't care about the heading
                assert np.allclose(known_correspondence.robot_pos(), np.array([x, y]))
                assert np.allclose(np.array([known_correspondence.landmark_pos(i) for i in range(4)]), np.array(landmarks), atol=0.2)
                prev_x, prev_y = x, y
        except Exception:
            pass
