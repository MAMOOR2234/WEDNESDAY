"""Text-to-speech output module for Wednesday assistant."""

import os
import platform
from .logger import setup_logger

logger = setup_logger(__name__)


class TextToSpeech:
    """Text-to-speech using pyttsx3 or Edge TTS."""

    def __init__(self, engine="pyttsx3", speed=150):
        """Initialize TTS engine."""
        self.engine_name = engine
        self.speed = speed
        self.engine = None
        self._init_engine()

    def _init_engine(self):
        """Initialize the TTS engine."""
        if self.engine_name == "pyttsx3":
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', self.speed)

                # Try to set a female voice if available
                voices = self.engine.getProperty('voices')
                if len(voices) > 1:
                    self.engine.setProperty('voice', voices[1].id)  # Female voice

                logger.info("Initialized pyttsx3 TTS engine")
            except ImportError:
                logger.warning("pyttsx3 not available, falling back to edge-tts")
                self.engine_name = "edge-tts"
                self._init_edge_tts()
            except Exception as e:
                logger.warning(f"pyttsx3 error: {e}, falling back to edge-tts")
                self.engine_name = "edge-tts"
                self._init_edge_tts()

        if self.engine_name == "edge-tts":
            self._init_edge_tts()

    def _init_edge_tts(self):
        """Initialize Edge TTS."""
        try:
            import edge_tts
            self.edge_tts = edge_tts
            logger.info("Initialized edge-tts TTS engine")
        except ImportError:
            logger.error("edge-tts not available")
            self.edge_tts = None

    def speak(self, text):
        """Speak text aloud."""
        if not text:
            return

        # Limit text length for safety
        text = text[:1000]

        if self.engine_name == "pyttsx3":
            self._speak_pyttsx3(text)
        elif self.engine_name == "edge-tts":
            self._speak_edge_tts(text)
        else:
            logger.warning("No TTS engine available")

    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.debug(f"Spoke: {text[:50]}...")
        except Exception as e:
            logger.error(f"pyttsx3 speak error: {e}")

    def _speak_edge_tts(self, text):
        """Speak using edge-tts."""
        try:
            import asyncio
            import tempfile

            async def _async_speak():
                from edge_tts import Communicate

                # Create temporary file for audio
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    temp_path = tmp.name

                try:
                    communicate = Communicate(text, voice="en-US-AriaNeural")
                    await communicate.save(temp_path)

                    # Play audio based on platform
                    if platform.system() == "Windows":
                        os.startfile(temp_path)
                    elif platform.system() == "Darwin":
                        os.system(f"afplay {temp_path}")
                    else:
                        os.system(f"ffplay -nodisp -autoexit {temp_path}")

                    logger.debug(f"Spoke via edge-tts: {text[:50]}...")
                finally:
                    # Clean up temp file after a delay
                    import time
                    time.sleep(5)
                    try:
                        os.unlink(temp_path)
                    except:
                        pass

            asyncio.run(_async_speak())
        except Exception as e:
            logger.error(f"edge-tts speak error: {e}")
            print(f"[TTS error: {e}]")
