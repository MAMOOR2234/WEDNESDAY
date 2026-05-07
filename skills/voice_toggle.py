"""Voice switching skill for Wednesday — male/female TTS voice."""
import sys
import os
from pathlib import Path

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill

CONFIG = Path(__file__).parent.parent / "assistant_workspace" / "voice_pref.txt"
CONFIG.parent.mkdir(exist_ok=True)


class Skill(BaseSkill):
    name = "Voice Toggle"
    description = "Switch between male and female TTS voices"

    def execute(self, args):
        target = args.get("voice", "").lower().strip()

        if target not in ("male", "female", "toggle"):
            current = self._current()
            return f"Current voice: {current}. Say 'switch to female voice' or 'use male voice'."

        if target == "toggle":
            target = "male" if self._current() == "female" else "female"

        CONFIG.write_text(target, encoding="utf-8")
        return f"Switched to {target} voice. You'll hear it on my next reply."

    def _current(self):
        if CONFIG.exists():
            return CONFIG.read_text(encoding="utf-8").strip() or "female"
        return "female"
