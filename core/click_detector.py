import time
import math
import pyautogui
from core.config import CLICK_THRESHOLD, CLICK_DELAY

# Detects mouse click based on distance between fingers
last_click = 0

def detect_click(x1, y1, x2, y2, frame):
    """
    Calculates distance between index finger and thumb.
    Triggers a mouse click if the distance is below a threshold.
    """
    global last_click
    dist = math.hypot(x2 - x1, y2 - y1)

    if dist < CLICK_THRESHOLD:
        if time.time() - last_click > CLICK_DELAY:
            pyautogui.click()
            last_click = time.time()
            return True
    return False
