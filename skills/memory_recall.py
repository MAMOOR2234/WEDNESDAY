"""Remember/recall skill for Wednesday — stash and recall arbitrary text."""
import sys
import json
from pathlib import Path

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill

WORKSPACE = Path(__file__).parent.parent / "assistant_workspace"
WORKSPACE.mkdir(exist_ok=True)
STORE = WORKSPACE / "remembered.json"


def _load():
    if STORE.exists():
        try: return json.loads(STORE.read_text(encoding="utf-8"))
        except Exception: return []
    return []


def _save(items):
    STORE.write_text(json.dumps(items, indent=2), encoding="utf-8")


class Skill(BaseSkill):
    name = "Memory Recall"
    description = "Remember things and recall them later (\"remember that...\")"

    def execute(self, args):
        action = args.get("action", "list")
        text   = args.get("text", "").strip()

        if action == "remember":
            if not text:
                return "What do you want me to remember?"
            items = _load()
            items.append(text)
            _save(items)
            return f"Got it — remembering: \"{text}\""

        elif action == "recall" or action == "list":
            items = _load()
            if not items:
                return "I don't have anything saved yet."
            if len(items) == 1:
                return f"You told me to remember: {items[0]}"
            return "Here's what I'm holding onto:\n" + "\n".join(f"  • {x}" for x in items)

        elif action == "forget":
            if text:
                items = _load()
                items = [x for x in items if text.lower() not in x.lower()]
                _save(items)
                return f"Forgot anything matching '{text}'"
            else:
                _save([])
                return "Cleared everything I was remembering."
            
        elif action == "clear":
            _save([])
            return "Cleared everything I was remembering."
        if not action:
            return "Please specify an action"
        

        return f"Unknown action: {action}"
