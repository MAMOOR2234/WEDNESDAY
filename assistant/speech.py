"""Voice input for Wednesday — sounddevice record → WAV → Google STT."""

import wave
import tempfile
import os
import numpy as np
from .logger import setup_logger

logger = setup_logger(__name__)

RATE        = 16000
CHUNK       = 1024
SILENCE_RMS = 150    # RMS below this counts as silence
SPEECH_RMS  = 350    # RMS above this = speech has started


def listen(wait_for_speech=8, max_duration=20, pause_threshold=2.5):
    """
    Record from mic until silence, transcribe with Google.
    Returns text string or None.
    """
    try:
        import sounddevice as sd
        import speech_recognition as sr
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return None

    silent_limit   = int(pause_threshold * RATE / CHUNK)
    max_chunks     = int(max_duration    * RATE / CHUNK)
    wait_chunks    = int(wait_for_speech * RATE / CHUNK)

    frames         = []
    silent_chunks  = 0
    speech_started = False

    logger.info("Mic open — waiting for speech...")

    try:
        with sd.InputStream(samplerate=RATE, channels=1, dtype="int16",
                            blocksize=CHUNK) as stream:
            # Wait for speech to begin
            for _ in range(wait_chunks):
                data, _ = stream.read(CHUNK)
                rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))
                if rms > SPEECH_RMS:
                    speech_started = True
                    frames.append(data.copy())
                    logger.info("Speech detected — recording...")
                    break

            if not speech_started:
                logger.info("No speech in wait window")
                return None

            # Record until pause_threshold of silence
            for _ in range(max_chunks):
                data, _ = stream.read(CHUNK)
                frames.append(data.copy())
                rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))
                if rms < SILENCE_RMS:
                    silent_chunks += 1
                    if silent_chunks >= silent_limit:
                        break
                else:
                    silent_chunks = 0

    except Exception as e:
        logger.error(f"Mic error: {e}")
        return None

    if not frames:
        return None

    # Write to temp WAV file
    tmp_path = None
    try:
        audio_np = np.concatenate(frames, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name

        with wave.open(tmp_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)       # int16 = 2 bytes
            wf.setframerate(RATE)
            wf.writeframes(audio_np.tobytes())

        logger.info("Transcribing...")
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.pause_threshold  = 1.0

        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language="en-US")
        logger.info(f"Transcribed: {text}")
        return text

    except sr.UnknownValueError:
        logger.warning("Google could not understand the audio — speak clearly and try again")
        return None
    except sr.RequestError as e:
        logger.warning(f"Google API error: {e}")
        return None
    except Exception as e:
        logger.warning(f"Transcription error: {type(e).__name__}: {e}")
        return None
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


class SpeechRecognizer:
    """Backward-compat wrapper."""
    def listen(self, timeout=12):
        return listen(wait_for_speech=timeout, max_duration=20, pause_threshold=2.5)
