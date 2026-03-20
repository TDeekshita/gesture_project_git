import cv2
import mediapipe as mp

# Detects hand landmarks using MediaPipe
class HandTracker:
    """
    Detects and tracks hand landmarks using MediaPipe.
    """
    def __init__(self, max_hands=1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands)
        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):
        """
        Processes the frame to detect hand landmarks.

        Returns:
            hand landmarks of the first detected hand (if any), else None.
        """
        # Convert frame to RGB (required by MediaPipe)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            self.drawer.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
            return hand
        return None
