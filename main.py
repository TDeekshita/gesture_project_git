"""
Gesture Controlled Virtual Mouse

Features:
- Cursor movement using hand tracking
- Click detection using finger distance
- Scroll and zoom using gestures
- Voice control for brightness and volume
- Multi-threaded system (gesture + voice)

Exit:
- Press ESC or say 'stop'
"""

import cv2
import pyautogui
import math
import threading
import time

from core.hand_tracker import HandTracker
from core.cursor_control import move_cursor
from core.click_detector import detect_click
from core.scroll import ScrollController
from core.zoom import ZoomController
from utils.draw_box import get_control_box, draw_box
from core.voice_control import VoiceController

running = True

# Initialize controllers
voice_ctrl = VoiceController()
scroll_ctrl = ScrollController()
zoom_ctrl = ZoomController()

# Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access camera")
    exit()
tracker = HandTracker()
screen_w, screen_h = pyautogui.size()

# Background thread for continuous voice command processing
# ----------------- Voice thread -----------------
def voice_thread():
    global running
    while running:
        command = voice_ctrl.listen_command()
        if command:
            if any(word in command for word in ["stop", "exit", "end"]):
                print("Stopping system...")
                running = False
                break
            status = voice_ctrl.handle_command(command)
            if status:
                print("Voice Command:", status)  # optional log
        time.sleep(0.1)

# Start voice listener thread
t = threading.Thread(target=voice_thread, daemon=True)
t.start()

# Main loop for real-time hand tracking and gesture control
# ----------------- Main loop -----------------
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Draw control box
    box = get_control_box(w, h)
    draw_box(frame, box)

    hand = tracker.detect(frame)
    if hand:
        # Finger landmarks
        index = hand.landmark[8]
        thumb = hand.landmark[4]
        middle = hand.landmark[12]
        ring = hand.landmark[16]
        pinky = hand.landmark[20]

        # Convert to frame pixels
        x_i, y_i = int(index.x * w), int(index.y * h)
        x_t, y_t = int(thumb.x * w), int(thumb.y * h)
        x_m, y_m = int(middle.x * w), int(middle.y * h)
        x_r, y_r = int(ring.x * w), int(ring.y * h)
        x_p, y_p = int(pinky.x * w), int(pinky.y * h)

        # Clamp inside control box
        left, right, top, bottom = box
        x_clamped = min(max(x_i, left), right)
        y_clamped = min(max(y_i, top), bottom)

        # Map hand position from camera frame to actual screen coordinates
        screen_x = (x_clamped - left) * screen_w / (right - left)
        screen_y = (y_clamped - top) * screen_h / (bottom - top)

        # Move cursor
        move_cursor(screen_x, screen_y)

        # CLICK detection (Index + Thumb)
        # Detect click using distance between index finger and thumb
        clicked = detect_click(x_i, y_i, x_t, y_t, frame)
        if clicked:
            cv2.putText(frame, "CLICK!", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # ---------- FINGERS OPEN STATUS ----------
        # Determine which fingers are open (1 = open, 0 = closed)
        fingers_open = []
        for tip_id, pip_id in zip([4, 8, 12, 16, 20], [2, 6, 10, 14, 18]):
            if hand.landmark[tip_id].y < hand.landmark[pip_id].y:
                fingers_open.append(1)
            else:
                fingers_open.append(0)

        # ---------- SCROLL ----------
        # Handle scroll gesture based on finger states
        scroll_status = scroll_ctrl.update(fingers_open)
        if scroll_status:
            cv2.putText(frame, scroll_status, (50, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        # ---------- ZOOM ----------
        # Handle zoom gesture based on finger distance
        zoom_status = zoom_ctrl.update((x_t, y_t), (x_p, y_p), fingers_open)
        if zoom_status:
            cv2.putText(frame, zoom_status, (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    # Show frame
    cv2.imshow("Gesture Mouse Control (Modular)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        print("ESC pressed. Exiting...")
        running = False
        break

cap.release()
cv2.destroyAllWindows()


