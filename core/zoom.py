import pyautogui
import time
import math

class ZoomController:
    """
    Controls zoom actions based on distance between thumb and pinky fingers.
    """

    def __init__(self):
        self.COOLDOWN = 0.2  # seconds
        self.last_zoom_time = 0
        self.CLOSE_THRESHOLD = 40   # distance to trigger zoom in
        self.FAR_THRESHOLD = 120    # distance to trigger zoom out

    def update(self, thumb_tip, pinky_tip, fingers_extended):
        """
        Args:
            thumb_tip (tuple): (x, y) coordinates of thumb tip
            pinky_tip (tuple): (x, y) coordinates of pinky tip
            fingers_extended (list): List of 5 ints (1 = open, 0 = closed)

        Returns:
            str: "ZOOM IN", "ZOOM OUT", or None
        """
        current_time = time.time()
        if current_time - self.last_zoom_time < self.COOLDOWN:
            return None

        # Calculate distance between thumb and pinky
        distance = math.hypot(thumb_tip[0]-pinky_tip[0], thumb_tip[1]-pinky_tip[1])

        # Fully open hand → no zoom
        if sum(fingers_extended) == 5:
            return None

        # Fingers close → zoom in
        if distance < self.CLOSE_THRESHOLD:
            pyautogui.hotkey('ctrl', '+')
            self.last_zoom_time = current_time
            return "ZOOM IN"
        elif distance > self.FAR_THRESHOLD:
            # Fingers apart but hand not fully open → zoom out
            pyautogui.hotkey('ctrl', '-')
            self.last_zoom_time = current_time
            return "ZOOM OUT"

        return None
