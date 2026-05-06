"""Keyboard automation skill for Wednesday."""

import time
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Type text and keyboard automation."""

    name = "Keyboard Control"
    description = "Type text and control keyboard"

    def execute(self, args):
        """Execute keyboard action."""
        action = args.get("action", "type")
        text = args.get("text", "")

        if action == "type":
            if not text:
                return "No text specified"
            return self._type_text(text)
        else:
            return f"Unknown action: {action}"

    def _type_text(self, text):
        """Type text on the screen."""
        try:
            import pyautogui

            # Add delay to ensure focus
            time.sleep(1)

            # Type the text
            pyautogui.typewrite(text)

            return f"Typed: {text[:50]}..."
        except ImportError:
            return "pyautogui not installed"
        except Exception as e:
            return f"Failed to type text: {e}"
