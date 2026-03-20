# Gesture and Voice Controlled Virtual Mouse

A real-time human-computer interaction system that enables hands-free control using computer vision and speech recognition.

---

## Features

- Cursor movement using hand tracking
- Click detection using finger distance
- Scroll control using gestures
- Zoom control using hand distance
- Voice control for brightness and volume
- Multi-threaded execution (gesture + voice)

---

## Technologies

- OpenCV
- MediaPipe
- PyAutoGUI
- SpeechRecognition
- PyCAW
- screen-brightness-control

---

## Project Structure
```
gesture_project_git/

├── core/
├── utils/
├── main.py
├── requirements.txt
└── .gitignore
```
---

## Installation

```bash
git clone https://github.com/TDeekshita/gesture_project_git.git
cd gesture_project_git
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

---

## Controls

**Gesture**

- Move finger → Cursor
- Thumb + Index → Click
- Open hand → Scroll up
- Closed fingers → Scroll down
- Thumb + Pinky distance → Zoom

**Voice**

- Increase / Decrease brightness
- Increase / Decrease volume
- Stop → Exit
---

## Exit

- Press ESC
- OR say "stop" or "exit"

---

## Author

Deekshita Totapally 
