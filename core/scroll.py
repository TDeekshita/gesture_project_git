import pyautogui

class ScrollController:
    """
    Controls vertical scrolling based on hand gesture (finger states).
    """

    def __init__(self):
        self.SCROLL_AMOUNT = 50  # pixels per scroll

    def update(self, fingers_open):
        """
        Args:
            fingers_open: list of 5 ints, 1 = finger up, 0 = down
        Returns:
            str: "SCROLL UP" or "SCROLL DOWN" or None
        """

        # All fingers wide open → scroll up
        if sum(fingers_open) == 5:
            pyautogui.scroll(self.SCROLL_AMOUNT)
            return "SCROLL UP"

        # Most fingers closed → scroll down
        elif sum(fingers_open) <= 1:  # only 0 or 1 finger up
            pyautogui.scroll(-self.SCROLL_AMOUNT)
            return "SCROLL DOWN"

        # Fingers in between → do nothing
        return None
