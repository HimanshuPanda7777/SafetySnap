
import cv2
import numpy as np
from PIL import Image
import io

def detect_ppe(image_path: str):
    """
    Dummy PPE detection using color thresholding.
    Returns:
        labels: list of detected PPE
        bbox: dict with x, y, w, h (normalized 0-1)
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return [], {}

    labels = []
    height, width, _ = img.shape

    # Example: detect yellow helmet (dummy)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        labels.append("helmet")
        x, y, w, h = cv2.boundingRect(contours[0])
        bbox = {"x": x/width, "y": y/height, "w": w/width, "h": h/height}
    else:
        bbox = {"x": 0, "y": 0, "w": 0, "h": 0}

    # Example: assume vest always detected
    labels.append("vest")
    if "w" not in bbox:
        bbox = {"x":0, "y":0, "w":0, "h":0}

    return labels, bbox
