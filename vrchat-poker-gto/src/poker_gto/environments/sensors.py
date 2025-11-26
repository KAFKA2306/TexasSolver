"""Sensors for VRChat Poker Environment."""

from typing import Any, override

import cv2
import mss
import numpy as np
import pytesseract
from pamiq_core import Sensor

from ..data.observations import GamePhase, PokerObservation


class ScreenCaptureSensor(Sensor[np.ndarray]):
    """Captures a specific region of the screen."""

    def __init__(self, region: dict[str, int] | None = None):
        """Initialize screen capture.

        Args:
            region: Dictionary with 'top', 'left', 'width', 'height'.
                    Defaults to a generic 800x600 window if None.
        """
        super().__init__()
        self.sct = mss.mss()
        self.region = region or {"top": 100, "left": 100, "width": 800, "height": 600}

    @override
    def read(self) -> np.ndarray:
        """Capture screen and return as numpy array (BGR)."""
        # mss returns BGRA, convert to BGR for opencv compatibility if needed
        # But here we just return the raw array, let OCR handle it.
        screenshot = self.sct.grab(self.region)
        return np.array(screenshot)


class PokerStateSensor(Sensor[PokerObservation]):
    """Parses screen image into PokerObservation using OCR."""

    def __init__(self, screen_sensor: ScreenCaptureSensor):
        super().__init__()
        self.screen_sensor = screen_sensor

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for OCR."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    @override
    def read(self) -> PokerObservation:
        """Read screen and parse poker state."""
        image = self.screen_sensor.read()
        processed = self._preprocess(image)

        # TODO: In a real implementation, we would crop specific regions
        # for cards, pot, stack before passing to OCR for speed and accuracy.
        # For this prototype, we assume we can extract text from the whole image
        # or that the image IS the relevant region.

        text = pytesseract.image_to_string(processed)

        # Mock parsing logic for prototype
        # In reality, we need robust regex parsing here.
        return PokerObservation(
            game_phase=GamePhase.FLOP,  # Mock
            pot_size=50.0,  # Mock
            effective_stack=200.0,  # Mock
            hole_cards=("As", "Kh"),  # Mock
            board_cards=["Qs", "Jh", "2h"],  # Mock
            position="IP",  # Mock
            action_history=[],
            timestamp=0.0,
        )
