import cv2
from core.config import CONTROL_BOX_PERCENT

def get_control_box(frame_w, frame_h):
    """
    Calculates the active control area within the frame.

    Returns:
        tuple: (left, right, top, bottom) boundaries
    """
    left = int(frame_w * CONTROL_BOX_PERCENT)
    right = int(frame_w * (1 - CONTROL_BOX_PERCENT))
    top = int(frame_h * CONTROL_BOX_PERCENT)
    bottom = int(frame_h * (1 - CONTROL_BOX_PERCENT))
    return left, right, top, bottom

def draw_box(frame, box):
    """
    Draws a rectangular control box on the frame.
    """
    left, right, top, bottom = box
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)
