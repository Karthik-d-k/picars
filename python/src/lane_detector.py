import cv2
import numpy as np
import torch
import torch.nn.functional as F
from camera_geometry import CameraGeometry


class LaneDetector:
    def __init__(
        self, model_path="../assests/model.pth", lane_width=0.36, *args, **kwargs
    ):
        self.lane_width = lane_width
        self.cam_geom = CameraGeometry(*args, **kwargs)
        self.cut_v, self.grid = self.cam_geom.precompute_grid()
        self.model = torch.load(model_path, map_location=torch.device("cpu"))
        self.model.eval()
        self.mean_residuals_thresh = 15

    def create_preprocessor(self, cv_image):
        # convert opencv output from BGR to RGB
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(
            image,
            (self.cam_geom.image_width, self.cam_geom.image_height),
            interpolation=cv2.INTER_AREA,
        )
        image_tensor = image.transpose(2, 0, 1).astype("float32") / 255.0
        input_batch = torch.from_numpy(image_tensor).unsqueeze(0)

        return input_batch

    def predict(self, input_batch):
        with torch.no_grad():
            out = F.softmax(self.model(input_batch), dim=1).numpy()
            background, left, right = out[0, 0, :, :], out[0, 1, :, :], out[0, 2, :, :]

        return background, left, right

    def fit_poly(self, probs, prob_thresh=0.3):
        probs_flat = np.ravel(probs[self.cut_v :, :])
        mask = probs_flat > prob_thresh
        if mask.sum() > 0:
            coeffs = np.polyfit(
                self.grid[:, 0][mask], self.grid[:, 1][mask], deg=3, w=probs_flat[mask]
            )
        else:
            coeffs = np.array([0.0, 0.0, 0.0, 0.0])

        return np.poly1d(coeffs)

    def get_fit_and_probs(self, cv_image):
        input_batch = self.create_preprocessor(cv_image)
        _, left, right = self.predict(input_batch)
        left_poly = self.fit_poly(left)
        right_poly = self.fit_poly(right)

        return left_poly, right_poly, left, right

    def fit_line_v_of_u(self, probs, thres):
        v_list, u_list = np.nonzero(probs > thres)
        if v_list.size == 0:
            return None
        coeffs, residuals, _, _, _ = np.polyfit(u_list, v_list, deg=1, full=True)

        mean_residuals = residuals / len(u_list)
        if mean_residuals > self.mean_residuals_thresh:
            return None
        else:
            return np.poly1d(coeffs)

    def get_intersection(self, line1, line2):
        xm_per_pix = self.lane_width / self.cam_geom.image_width
        m1, c1 = line1
        m2, c2 = line2
        if m1 == m2:
            return None
        u_i = (c2 - c1) / (m1 - m2)
        v_i = m1 * u_i + c1
        return u_i * xm_per_pix, v_i * xm_per_pix

    def __call__(self, cv_image):
        left_poly, right_poly, left_probs, right_probs = self.get_fit_and_probs(
            cv_image
        )
        line_left = self.fit_line_v_of_u(left_probs, 0.1)
        line_right = self.fit_line_v_of_u(right_probs, 0.1)
        lane_center, _ = self.get_intersection(line_left, line_right)
        lane_deviation = lane_center - (self.lane_width / 2)

        return (
            left_poly,
            right_poly,
            left_probs,
            right_probs,
            lane_center,
            lane_deviation,
        )
