import numpy as np


class KnownCorrespondence:
    """
    Class that calculates the EKF-SLAM with known correspondence
    """

    UNINITIALIZED = 1e6

    def __init__(self, init: np.ndarray, num_landmarks: int, Qt: np.ndarray, Rt: np.ndarray) -> None:
        """Initializes calculator for 2D EKF-SLAM with known correspondence

        :param init: Array for starting robot position with shape (3,) [x, y, absolute heading in radians]
        :param num_landmarks: Number of total landmarks
        :param Qt: Measurement noise model (2x2)
        :param Rt: Movement nose model (3x3)
        """
        self.Qt = Qt  # sensor model noise parameters
        self.Rt = Rt  # movement model noise parameters

        self.num_landmarks = num_landmarks

        self.mean = np.append(np.array(init), np.zeros((2 * num_landmarks)))
        self.cov = np.eye((2 * num_landmarks) + 3) * self.UNINITIALIZED
        self.cov[:3, :3] = np.zeros((3, 3))

    def robot_pos(self) -> np.ndarray:
        """Returns the position of the robot

        :return: the position of the robot as a (2, ) numpy array
        """
        return self.mean[:2]

    def landmark_pos(self, landmark_id: int) -> np.ndarray:
        """Returns the position of the corresponding landmark, or None if the landmark has not been observed

        :param landmark_id: the ID of the landmark
        :return: the position of the landmark as a (2, ) numpy array
        """
        if self.cov[2 * landmark_id + 3, 2 * landmark_id + 3] == self.UNINITIALIZED:
            return None
        else:
            return self.mean[2 * landmark_id + 3 : 2 * landmark_id + 5]

    def predict(self, u_t: np.ndarray) -> None:
        """Prediction step of robot state after recieving movement vector; updates robot position and heading only

        u_t[0] = magnitude of movement ()
        u_t[1] = angle of movement in radians

        :param u_t: Movement vector for the robot (2x1)
        """
        assert u_t.shape == (2,)
        n = self.mean.shape[0]

        mu = self.mean
        cov = self.cov

        rot = u_t[1]
        trans = u_t[0]

        # calculate pose update from odometry
        pose_update = [trans * np.cos(rot), trans * np.sin(rot), rot]

        F_x = np.append(np.eye(3), np.zeros((3, n - 3)), axis=1)

        # Predict new state
        mu_bar = mu + (F_x.T).dot(pose_update)

        # Define motion model Jacobian
        J = np.array([[0, 0, -trans * np.sin(rot)], [0, 0, trans * np.cos(rot)], [0, 0, 0]])
        G = np.eye(n) + (F_x.T).dot(J).dot(F_x)

        # Predict new covariance
        cov_bar = G.dot(cov).dot(G.T) + (F_x.T).dot(self.Rt).dot(F_x)

        self.cov = cov_bar
        self.mean = mu_bar

    def update(self, z: np.ndarray) -> None:
        """Update robot and landmark locations based on observations of landmarks

        :param z: 2D np array of length K, where K is the number of landmarks observed.
            Each row is a 3D vector [distance, angle, landmark ID]
        """
        assert len(z.shape) == 2
        assert z.shape[1] == 3

        cov = self.cov
        mu = self.mean

        N = self.mean.shape[0]

        for k in range(z.shape[0]):
            r = z[k, 0]
            theta = z[k, 1]
            j = int(z[k, 2])
            assert j < self.num_landmarks, "Landmark ID out of range"

            # if landmark has not been observed before
            if cov[2 * j + 3, 2 * j + 3] == self.UNINITIALIZED and cov[2 * j + 4, 2 * j + 4] >= self.UNINITIALIZED:
                # define landmark estimate as current measurement
                mu[2 * j + 3] = mu[0] + r * np.cos(theta)
                mu[2 * j + 4] = mu[1] + r * np.sin(theta)

            # compute expected observation
            delta = np.array([mu[2 * j + 3] - mu[0], mu[2 * j + 4] - mu[1]])
            q = delta.T.dot(delta)
            sq = np.sqrt(q)
            pred_theta = np.arctan2(delta[1], delta[0])

            z_hat = np.array([[sq], [pred_theta]])

            # calculate Jacobian
            F = np.zeros((5, N))
            F[:3, :3] = np.eye(3)
            F[3, 2 * j + 3] = 1
            F[4, 2 * j + 4] = 1
            H_z = np.array(
                [
                    [-sq * delta[0], -sq * delta[1], 0, sq * delta[0], sq * delta[1]],
                    [delta[1], -delta[0], -q, -delta[1], delta[0]],
                ],
                dtype="float",
            )
            H = 1 / q * H_z.dot(F)

            # calculate Kalman gain
            K = cov.dot(H.T).dot(np.linalg.pinv(H.dot(cov).dot(H.T) + self.Qt))

            # calculate difference between expected and real observation
            z_dif = np.array([[r], [theta]]) - z_hat
            z_dif = (z_dif + np.pi) % (2 * np.pi) - np.pi

            mu = mu + np.squeeze(K.dot(z_dif))
            cov = (np.eye(N) - K.dot(H)).dot(cov)

        self.mean = mu
        self.cov = cov
