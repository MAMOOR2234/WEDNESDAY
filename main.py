#!/usr/bin/env python3
"""
Wednesday - Windows Desktop AI Assistant
Enhanced with JARVIS-style modular architecture
Main entry point
"""

import sys
import os
import queue
import threading

# Force UTF-8 so emojis don't crash on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add assistant module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.core import WednesdayCore
from assistant.logger import setup_logger
from assistant.clap_detector import ClapDetector

logger = setup_logger(__name__)

_CLAP_CMD = "__clap_wake__"


class WednesdayInterface:
    """Command-line interface for Wednesday."""

    def __init__(self):
        self.core = WednesdayCore()
        self.running = True
        self._tts = None
        self._cmd_queue = queue.Queue()

        # Start clap detector
        self._clap = ClapDetector(on_double_clap=self._on_double_clap)
        self._clap.start()

        logger.info("Wednesday initialized successfully")
        print("\n[Wednesday AI Assistant]")
        print("=" * 50)
        print("Yo! I'm Wednesday, your AI friend")
        print("What's up? Type something or ask for help")
        print("(Double-clap to wake me hands-free)")
        print("=" * 50 + "\n")

    # ── Clap callback ──────────────────────────────────────────────────────────

    def _on_double_clap(self):
        print("\n\n[** CLAP DETECTED **]")
        print("Wednesday: Sup? I'm listening.\n")
        self.speak("Sup? I'm listening.")
        self._cmd_queue.put(_CLAP_CMD)

    # ── Input ─────────────────────────────────────────────────────────────────

    def _input_thread(self):
        """Read keyboard input in a background thread."""
        while self.running:
            try:
                text = input("You: ").strip()
                if text:
                    self._cmd_queue.put(text)
            except EOFError:
                self._cmd_queue.put("EOF")
                break
            except KeyboardInterrupt:
                break

    # ── Command processing ────────────────────────────────────────────────────

    def process_command(self, user_input):
        if not user_input or user_input == _CLAP_CMD:
            return

        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye', 'peace', 'later']:
            self.speak("Aight, catch you later! Stay awesome!")
            self.running = False
            return

        if user_input.lower() == 'help':
            self.show_help()
            return

        print("[*] Let me think about that...")
        response, skill_results = self.core.process_input(user_input)

        print(f"Wednesday: {response}\n")

        if skill_results:
            for result in skill_results:
                if result["status"] == "success":
                    print(f"[Done] {result['skill']}: {result.get('result', 'All set!')}\n")
                else:
                    print(f"[Oops] {result['skill']}: {result.get('error', 'Something went wrong')}\n")

        self.speak(response)

    def speak(self, text):
        try:
            if self._tts is None:
                from assistant.tts import TextToSpeech
                self._tts = TextToSpeech()
            self._tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def show_help(self):
        help_text = """
Wednesday - Your AI Homie

Here's what I can do for ya:

STUFF I CAN HANDLE:
- "Open Chrome" - Boom, browser open
- "Search for [thing]" - Google it for you
- "Open Word/Excel" - Launch apps
- "Close [app]" - Shut down whatever
- "Type [text]" - I'll type it out
- "What time is it?" - Check the time
- "Tell me a joke" - Need a laugh? I got you
- "Save this to notes" - Store stuff for you

CLAP FEATURE:
- Double-clap anywhere to wake me up hands-free

COMMANDS:
- help: This message
- exit/quit: Peace out
- Or just ask me anything!
        """
        print(help_text)
        self.speak("Yo, I can open apps, search the web, type stuff, handle files, and just chat. Ask me anything! Or say exit to bounce.")

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        input_t = threading.Thread(target=self._input_thread, daemon=True, name="InputThread")
        input_t.start()

        try:
            while self.running:
                try:
                    cmd = self._cmd_queue.get(timeout=0.1)
                    if cmd == "EOF":
                        break
                    self.process_command(cmd)
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    print("\n[Interrupted]")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    print(f"Error: {e}")
        finally:
            self._clap.stop()
            print("\nWednesday offline. Have a great day!")
            logger.info("Wednesday session ended")


if __name__ == "__main__":
    assistant = WednesdayInterface()
    assistant.run()
