"""Reminders and notes skill for Wednesday."""

import json
from pathlib import Path
from datetime import datetime
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Manage reminders and notes."""

    name = "Reminders & Notes"
    description = "Create reminders and save notes"

    def __init__(self):
        """Initialize reminders skill."""
        workspace = Path(__file__).parent.parent / "assistant_workspace"
        self.reminders_file = workspace / "reminders.json"
        self.notes_file = workspace / "notes.json"
        self._ensure_files()

    def _ensure_files(self):
        """Ensure reminder files exist."""
        if not self.reminders_file.exists():
            self.reminders_file.write_text(json.dumps([]))
        if not self.notes_file.exists():
            self.notes_file.write_text(json.dumps([]))

    def execute(self, args):
        """Execute reminder/note action."""
        action = args.get("action", "create")
        reminder_type = args.get("type", "reminder")  # reminder or note

        if action == "create":
            return self._create(reminder_type, args)
        elif action == "list":
            return self._list(reminder_type)
        else:
            return f"Unknown action: {action}"

    def _create(self, reminder_type, args):
        """Create reminder or note."""
        content = args.get("content", "")

        if not content:
            return "No content specified"

        data = {
            "content": content,
            "created": datetime.now().isoformat(),
            "status": "active"
        }

        if reminder_type == "reminder":
            due = args.get("due_date")
            if due:
                data["due_date"] = due

            reminders = json.loads(self.reminders_file.read_text())
            reminders.append(data)
            self.reminders_file.write_text(json.dumps(reminders, indent=2))

            return f"Reminder set: {content}"
        else:
            notes = json.loads(self.notes_file.read_text())
            notes.append(data)
            self.notes_file.write_text(json.dumps(notes, indent=2))

            return f"Note saved: {content}"

    def _list(self, reminder_type):
        """List reminders or notes."""
        if reminder_type == "reminder":
            reminders = json.loads(self.reminders_file.read_text())
            if not reminders:
                return "No reminders"

            result = "Your reminders:\n"
            for i, r in enumerate(reminders, 1):
                result += f"{i}. {r['content']}"
                if "due_date" in r:
                    result += f" (due: {r['due_date']})"
                result += "\n"
            return result
        else:
            notes = json.loads(self.notes_file.read_text())
            if not notes:
                return "No notes"

            result = "Your notes:\n"
            for i, n in enumerate(notes, 1):
                result += f"{i}. {n['content']}\n"
            return result
