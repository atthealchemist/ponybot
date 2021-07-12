from PIL import Image
from io import BytesIO
import numpy as np
import cv2


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def crop_avatar_background(
    avatar,
    padding=10
):
    # load image
    img = cv2.imdecode(np.frombuffer(avatar.read(), np.uint8), 1)

    # img = cv2.imread(avatar)

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold to get just the pony
    _, thresh_gray = cv2.threshold(
        gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

    # find where the pony is and make a cropped region
    points = np.argwhere(thresh_gray == 0)  # find where the black pixels are
    # store them in x,y coordinates instead of row,col indices
    points = np.fliplr(points)
    # create a rectangle around those points
    x, y, w, h = cv2.boundingRect(points)
    # create a cropped region of the gray image
    crop = img[
        y - padding: y + h + padding * 5,
        x - padding: x + w + padding * 5
    ]

    # get the thresholded crop
    return cv2.imencode('.png', crop)[1].tobytes()
