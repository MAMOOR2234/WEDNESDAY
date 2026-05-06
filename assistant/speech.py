"""Voice input module for Wednesday assistant."""

import os
import sys
from .logger import setup_logger

logger = setup_logger(__name__)


class SpeechRecognizer:
    """Speech recognition using faster-whisper or fallback."""

    def __init__(self, engine="speech_recognition"):
        """Initialize speech recognizer."""
        self.engine = engine
        self.recognizer = None
        self.microphone = None
        self.pyaudio_available = False
        self._init_engine()

    def _init_engine(self):
        """Initialize the speech recognition engine."""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            try:
                self.microphone = sr.Microphone()
                self.pyaudio_available = True
                logger.info("Initialized speech_recognition with microphone support")
            except AttributeError as e:
                logger.warning(f"PyAudio not available: {e}")
                logger.warning("Microphone input will not be available")
                self.pyaudio_available = False
        except ImportError:
            logger.error("SpeechRecognition not available")
            self.recognizer = None

    def listen(self, timeout=10):
        """Listen for voice input and convert to text."""
        if not self.pyaudio_available or not self.recognizer or not self.microphone:
            logger.warning("Microphone not available - voice input disabled")
            return None

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("[Listening for voice...]")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

            # Try Google Speech Recognition (free)
            print("[Recognizing speech...]")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text

        except Exception as e:
            logger.warning(f"Speech recognition error: {e}")
            return None
