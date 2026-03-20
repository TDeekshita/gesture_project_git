import speech_recognition as sr
import screen_brightness_control as sbc
import pyautogui

# For volume control (Windows)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VoiceController:
    """
    Handles voice commands for system brightness and volume control.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Initialize system audio interface (PyCAW)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        

    def listen_command(self):
        """
        Listens to microphone input and converts speech to text.

        Returns:
            str: recognized command (lowercase) or None
        """
        try:
            with sr.Microphone() as source:
                print("Listening for command...")
                audio = self.recognizer.listen(source, phrase_time_limit=3)
        except Exception as e:
            print("Microphone error:", e)
            return None

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print("Command:", command)
            return command
        except:
            return None

    def handle_command(self, command):
        """
        Executes brightness or volume actions based on command.

        Returns:
            str: status message or None
        """
        if not command:
            return None

        # -------------------- BRIGHTNESS --------------------
        # Increase brightness
        if "increase brightness" in command:
            curr = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(min(curr + 10, 100))
            return "Brightness Increased"
        
        # Decrease brightness
        elif "decrease brightness" in command:
            curr = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(curr - 10, 0))
            return "Brightness Decreased"

        # -------------------- VOLUME ------------------------
        # Increase volume
        elif "increase volume" in command:
            vol = self.volume.GetMasterVolumeLevelScalar()
            self.volume.SetMasterVolumeLevelScalar(min(vol + 0.1, 1.0), None)
            return "Volume Up"
        # Decrease volume

        elif "decrease volume" in command:
            vol = self.volume.GetMasterVolumeLevelScalar()
            self.volume.SetMasterVolumeLevelScalar(max(vol - 0.1, 0.0), None)
            return "Volume Down"

        return None
