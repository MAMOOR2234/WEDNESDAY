#!/usr/bin/env python3
"""
Wednesday AI Assistant - Smart Launcher
Detects display and launches appropriate mode
"""

import sys
import os
import platform

# Add assistant module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.logger import setup_logger

logger = setup_logger(__name__)


def has_display():
    """Check if display is available."""
    if platform.system() == "Windows":
        return True  # Windows always has display

    # Linux/Mac check
    return os.environ.get("DISPLAY") is not None


def launch_gui():
    """Launch GUI mode."""
    try:
        from assistant.core import WednesdayCore
        from assistant.gui import launch_gui as gui_launch

        print("[*] Initializing Wednesday Core Engine...")
        core = WednesdayCore()

        print("[*] Launching GUI Interface...")
        logger.info("Launching GUI mode")
        gui_launch(core)

    except Exception as e:
        print(f"\n[ERROR] GUI Launch Failed: {e}")
        logger.error(f"GUI launch error: {e}")
        return False

    return True


def launch_cli():
    """Launch CLI mode."""
    try:
        from assistant.core import WednesdayCore
        from assistant.speech import SpeechRecognizer
        from assistant.tts import TextToSpeech

        print("\n[*] Initializing Wednesday Core Engine...")
        core = WednesdayCore()

        print("\n[Wednesday AI Assistant]")
        print("=" * 50)
        print("Yo! I'm Wednesday, your AI friend")
        print("Type commands or ask for help")
        print("Type 'exit' to quit")
        print("=" * 50 + "\n")

        logger.info("Launching CLI mode")

        # Main loop
        while True:
            try:
                user_input = input("[You] ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    print("\n[Wednesday] Aight, catch you later!")
                    break

                if user_input.lower() == 'help':
                    print("""
Commands:
- Type anything to chat
- 'help' - This message
- 'exit' - Close Wednesday
- Or just ask me anything!
                    """)
                    continue

                print("\n[*] Wednesday thinking...\n")
                response, skills = core.process_input(user_input)
                print(f"[Wednesday] {response}\n")

                if skills:
                    for skill in skills:
                        print(f"  [Skill] {skill.get('skill', 'unknown')}\n")

            except KeyboardInterrupt:
                print("\n\n[Wednesday] Aight, see you!")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}\n")
                logger.error(f"Error in CLI: {e}")

        return True

    except Exception as e:
        print(f"\n[ERROR] CLI Launch Failed: {e}")
        logger.error(f"CLI launch error: {e}")
        return False


def main():
    """Smart launcher - tries GUI, falls back to CLI."""
    print("\n" + "=" * 50)
    print("  Wednesday AI Assistant")
    print("=" * 50 + "\n")

    # Check if we can use GUI
    if has_display():
        print("[*] Display detected. Attempting GUI launch...\n")

        try:
            import PyQt6
            if launch_gui():
                return 0
        except ImportError:
            print("[!] PyQt6 not available. Falling back to CLI...\n")
        except Exception as e:
            print(f"[!] GUI failed: {e}")
            print("[*] Falling back to CLI mode...\n")

    # Fall back to CLI
    print("[*] Using CLI Mode")
    print("[*] (For GUI mode, install PyQt6: pip install PyQt6)\n")

    if launch_cli():
        return 0
    else:
        print("\n[ERROR] Failed to launch Wednesday")
        return 1


if __name__ == "__main__":
    sys.exit(main())
