"""Visual awareness skill - screenshot and screen analysis."""

from pathlib import Path
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Take screenshots and analyze screen."""

    name = "Visual Awareness"
    description = "Take screenshots and analyze what's on screen"

    def execute(self, args):
        """Execute visual awareness command."""
        action = args.get("action", "screenshot")

        if action == "screenshot":
            return self._take_screenshot()
        elif action == "describe":
            return self._describe_screen()
        else:
            return f"Unknown action: {action}"

    def _take_screenshot(self):
        """Take a screenshot."""
        try:
            import pyautogui

            workspace = Path(__file__).parent.parent / "assistant_workspace"
            screenshot_path = workspace / f"screenshot_{Path.cwd().name}.png"

            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)

            return f"Screenshot saved to {screenshot_path}"
        except ImportError:
            return "pyautogui not installed for screenshots"
        except Exception as e:
            return f"Screenshot failed: {e}"

    def _describe_screen(self):
        """Describe what's on screen (requires OCR)."""
        try:
            import pyautogui

            # Take screenshot
            screenshot = pyautogui.screenshot()

            # Try to use OCR if available
            try:
                import pytesseract
                from PIL import Image

                text = pytesseract.image_to_string(screenshot)
                return f"Screen text:\n{text[:500]}"
            except ImportError:
                return "OCR not available (install pytesseract for text detection)"

        except Exception as e:
            return f"Screen analysis failed: {e}"
