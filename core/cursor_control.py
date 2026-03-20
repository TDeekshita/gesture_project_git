import pyautogui
from core.config import SCREEN_SPEED, SMOOTHING_ALPHA

prev_x, prev_y = 0, 0
screen_w, screen_h = pyautogui.size()


def move_cursor(frame_x, frame_y):
    """
    Moves the mouse cursor smoothly based on input coordinates.
    Applies exponential smoothing to reduce jitter.
    """
    global prev_x, prev_y

    frame_x *= SCREEN_SPEED
    frame_y *= SCREEN_SPEED

    # Apply exponential smoothing to reduce sudden cursor movements
    smooth_x = prev_x * (1 - SMOOTHING_ALPHA) + frame_x * SMOOTHING_ALPHA
    smooth_y = prev_y * (1 - SMOOTHING_ALPHA) + frame_y * SMOOTHING_ALPHA

    pyautogui.moveTo(smooth_x, smooth_y)

    prev_x, prev_y = smooth_x, smooth_y
