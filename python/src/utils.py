import time
import traceback

import cv2
import numpy as np
import rustimport.import_hook  # noqa: F401
from traffic_light import detect_traffic_light

import ruspy


def try_func(func):
    try:
        ruspy.main_init()
        func()
    except Exception as e:
        print(f"ERROR in {func.__name__}: {e}")
        traceback.print_exc()
    finally:
        print("FINAL RESET")
        ruspy.reset_mcu()


def create_video_capture(w=224, h=224, fps=10):
    vid_cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    vid_cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    vid_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    vid_cap.set(cv2.CAP_PROP_FPS, fps)

    return vid_cap


def detect_green(vid_cap, max_time_limit):
    start_time = time.time()

    while time.time() - start_time <= max_time_limit:
        # Run till Green light is detected
        ret, cv_image = vid_cap.read()
        if not ret:
            print("FRAME NOT CAPTURED")
            continue
        left = fill_left_img(cv_image)
        right = fill_right_img(left)
        bottom = fill_bottom_img(right)
        is_green, t_img = detect_traffic_light(bottom)
        # cv2.imwrite("t_img.jpg", t_img)
        if not is_green:
            continue

        return True

    print("[TRAFFIC_LIGHT]: MAX TIME LIMIT EXCEEDED")

    return False


def fill_top_img(cv_img, top_percent=30):
    # Get the dimensions of the image
    height, width, _ = cv_img.shape
    # Calculate the number of rows to cut based on the percentage
    cut_rows = int((top_percent / 100) * height)
    # Create a new image filled with white color for the top half
    top_half = (
        np.ones((cut_rows, width, 3), dtype=np.uint8) * 255
    )  # 255 represents white color in RGB
    # Replace the top portion of the original image with the white half
    cv_img[:cut_rows, :] = top_half

    return cv_img


def fill_bottom_img(cv_img, top_percent=30):
    # Get the dimensions of the image
    height, width, _ = cv_img.shape
    # Calculate the number of rows to cut based on the percentage
    cut_rows = int((top_percent / 100) * height)
    # Create a new image filled with white color for the top half
    top_half = (
        np.ones((cut_rows, width, 3), dtype=np.uint8) * 255
    )  # 255 represents white color in RGB
    # Replace the top portion of the original image with the white half
    cv_img[-cut_rows:, :] = top_half

    return cv_img


def fill_left_img(cv_img, left_percent=30):
    # Get the dimensions of the image
    height, width, _ = cv_img.shape
    # Calculate the number of columns to cut based on the percentage
    cut_cols = int((left_percent / 100) * width)
    # Create a new image filled with white color for the left half
    left_half = (
        np.ones((height, cut_cols, 3), dtype=np.uint8) * 255
    )  # 255 represents white color in RGB
    # Replace the left portion of the original image with the white half
    cv_img[:, :cut_cols] = left_half

    return cv_img


def fill_right_img(cv_img, right_percent=30):
    # Get the dimensions of the image
    height, width, _ = cv_img.shape
    # Calculate the number of columns to cut based on the percentage
    cut_cols = int((right_percent / 100) * width)
    # Create a new image filled with white color for the right half
    right_half = (
        np.ones((height, cut_cols, 3), dtype=np.uint8) * 255
    )  # 255 represents white color in RGB
    # Replace the right portion of the original image with the white half
    cv_img[:, -cut_cols:] = right_half

    return cv_img


def crop_image_with_percentages(
    cv_img, left_percent=30, right_percent=30, bottom_percent=70, top_percent=0
):
    # Get the dimensions of the original image
    height, width, _ = cv_img.shape

    # Calculate the number of rows and columns to cut based on the percentages
    cut_left_cols = int((left_percent / 100) * width)
    cut_right_cols = int((right_percent / 100) * width)
    cut_top_rows = int((top_percent / 100) * height)
    cut_bottom_rows = int((bottom_percent / 100) * height)

    # Calculate the coordinates for cropping
    top_left_x = cut_left_cols
    top_left_y = cut_top_rows
    bottom_right_x = width - cut_right_cols
    bottom_right_y = height - cut_bottom_rows

    # Crop the image based on the calculated coordinates
    cropped_img = cv_img[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

    return cropped_img


if __name__ == "__main__":
    filenames = [
        "t_img",
    ]

    for filename in filenames:
        print(filename)
        # read image
        cv_img = cv2.imread(filename + ".jpg")
        # cv_img = fill_top_img(cv_img, 10)
        cv_img = fill_left_img(cv_img, 30)
        cv_img = fill_right_img(cv_img, 30)
        cv_img = fill_bottom_img(cv_img, 70)
        crop = crop_image_with_percentages(cv_img)
        # cv2.imwrite(filename + "white.jpg", cv_img)
        # cv2.imwrite(filename + "crop.jpg", crop)
        is_green, t_img = detect_traffic_light(crop)
        print(is_green)
        # cv2.imwrite("t_img.jpg", t_img)
