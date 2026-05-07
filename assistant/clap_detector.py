"""Background clap detector — double-clap to wake Wednesday."""

import threading
import time
import logging

logger = logging.getLogger(__name__)


class ClapDetector:
    # Raise THRESHOLD if too many false triggers; lower it if claps aren't detected.
    THRESHOLD = 500
    COOLDOWN  = 0.15   # min seconds between two detected claps
    WINDOW    = 0.7    # seconds within which 2 claps count as a double-clap
    CHUNK     = 512
    RATE      = 44100

    def __init__(self, on_double_clap=None):
        self.on_double_clap = on_double_clap
        self._running = False
        self._thread = None
        self.muted = False   # set True while TTS/voice is active to avoid false triggers

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True, name="ClapDetector")
        self._thread.start()
        logger.info("Clap detector started")

    def stop(self):
        self._running = False

    def _listen(self):
        try:
            import sounddevice as sd
            import numpy as np
        except ImportError:
            logger.warning("sounddevice/numpy not available — clap detection disabled")
            return

        clap_times = []
        last_clap = 0.0
        logger.info("Clap detector listening on mic...")

        def callback(indata, frames, time_info, status):
            nonlocal last_clap, clap_times
            rms = float(np.sqrt(np.mean(indata.astype(np.float32) ** 2)))
            now = time.time()

            if rms > self.THRESHOLD and (now - last_clap) > self.COOLDOWN and not self.muted:
                last_clap = now
                clap_times = [t for t in clap_times if now - t < self.WINDOW]
                clap_times.append(now)

                if len(clap_times) >= 2:
                    clap_times.clear()
                    if self.on_double_clap:
                        threading.Thread(target=self.on_double_clap, daemon=True).start()

        try:
            with sd.InputStream(
                samplerate=self.RATE,
                channels=1,
                dtype="int16",
                blocksize=self.CHUNK,
                callback=callback,
            ):
                while self._running:
                    time.sleep(0.05)
        except Exception as e:
            logger.warning(f"Mic unavailable — clap detection disabled: {e}")
