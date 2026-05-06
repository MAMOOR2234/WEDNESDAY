#!/usr/bin/env python3
"""
Wednesday - Windows Desktop AI Assistant
Enhanced with JARVIS-style modular architecture
Main entry point
"""

import sys
import os

# Force UTF-8 so emojis don't crash on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add assistant module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.core import WednesdayCore
from assistant.logger import setup_logger

logger = setup_logger(__name__)


class WednesdayInterface:
    """Command-line interface for Wednesday."""

    def __init__(self):
        """Initialize Wednesday."""
        self.core = WednesdayCore()
        self.running = True
        self._tts = None  # lazy-init once

        logger.info("Wednesday initialized successfully")
        print("\n[Wednesday AI Assistant]")
        print("=" * 50)
        print("Yo! I'm Wednesday, your AI friend")
        print("What's up? Type something or ask for help")
        print("=" * 50 + "\n")

    def get_user_input(self):
        """Get input from keyboard."""
        try:
            user_input = input("You: ").strip()
            if user_input:
                logger.info(f"Text input: {user_input}")
                return user_input
            return None
        except KeyboardInterrupt:
            return None
        except EOFError:
            return "EOF"  # sentinel so run() knows stdin is gone

    def process_command(self, user_input):
        """Process user command through core engine."""
        if not user_input:
            return

        # Handle exit commands
        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye', 'peace', 'later']:
            self.speak("Aight, catch you later! Stay awesome!")
            self.running = False
            return

        # Handle help command
        if user_input.lower() == 'help':
            self.show_help()
            return

        # Process with core engine
        print("[*] Let me think about that...")
        logger.info("Processing with core engine...")

        response, skill_results = self.core.process_input(user_input)

        # Display results
        print(f"Wednesday: {response}\n")

        # Show skill results if any
        if skill_results:
            for result in skill_results:
                if result["status"] == "success":
                    print(f"[Done] {result['skill']}: {result.get('result', 'All set!')}\n")
                else:
                    print(f"[Oops] {result['skill']}: {result.get('error', 'Something went wrong')}\n")

        # Speak response
        self.speak(response)

    def speak(self, text):
        """Convert text to speech."""
        try:
            if self._tts is None:
                from assistant.tts import TextToSpeech
                self._tts = TextToSpeech()
            self._tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")

    def show_help(self):
        """Display help information."""
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

COMMANDS:
- help: This message
- exit/quit: Peace out
- Or just ask me anything!

Wanna know what skills I got? Just ask!
        """
        print(help_text)
        self.speak("Yo, I can open apps, search the web, type stuff, handle files, and just chat. Ask me anything! Or say exit to bounce.")

    def run(self):
        """Main event loop."""
        try:
            while self.running:
                try:
                    user_input = self.get_user_input()
                    if user_input == "EOF":
                        # stdin is closed (e.g. piped input finished)
                        break
                    if user_input is None:
                        continue
                    self.process_command(user_input)
                except KeyboardInterrupt:
                    print("\n[Interrupted]")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            pass
        finally:
            print("\nWednesday offline. Have a great day!")
            logger.info("Wednesday session ended")


if __name__ == "__main__":
    assistant = WednesdayInterface()
    assistant.run()
