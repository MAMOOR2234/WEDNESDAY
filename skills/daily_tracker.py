"""Daily activity tracker - shows what you did today and what you're working on."""

import json
from datetime import datetime
from pathlib import Path
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Track and recall daily activity."""

    name = "Daily Tracker"
    description = "See what you did today, what you're working on, session history"

    def __init__(self):
        workspace = Path(__file__).parent.parent / "assistant_workspace"
        workspace.mkdir(exist_ok=True)
        self.activity_file = workspace / "daily_activity.json"
        self.logs_dir = Path(__file__).parent.parent / "logs"
        self._ensure_file()

    def _ensure_file(self):
        if not self.activity_file.exists():
            self.activity_file.write_text(json.dumps({"days": {}}))

    def execute(self, args):
        action = args.get("action", "summary")

        if action == "summary":
            return self.get_today_summary()
        elif action == "set_working_on":
            return self.set_working_on(args.get("task", ""))
        elif action == "get_working_on":
            return self.get_working_on()
        elif action == "log_activity":
            return self.log_activity(args.get("activity", ""))
        elif action == "set_mood":
            return self.set_mood(args.get("mood", ""), args.get("note", ""))
        elif action == "get_mood":
            return self.get_mood()
        elif action == "history":
            return self.get_session_history()
        else:
            return f"Unknown action: {action}"

    def set_mood(self, mood, note=""):
        """Save current mood to daily activity."""
        if not mood:
            return "What's the mood?"
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M")
        data = json.loads(self.activity_file.read_text())
        if today not in data["days"]:
            data["days"][today] = {}
        data["days"][today]["mood"] = {"mood": mood, "note": note, "time": now}
        if "mood_history" not in data["days"][today]:
            data["days"][today]["mood_history"] = []
        data["days"][today]["mood_history"].append({"mood": mood, "note": note, "time": now})
        self.activity_file.write_text(json.dumps(data, indent=2))
        return f"Got it, noted that you're feeling {mood}."

    def get_mood(self):
        """Return current mood."""
        today = datetime.now().strftime("%Y-%m-%d")
        data = json.loads(self.activity_file.read_text())
        mood_data = data["days"].get(today, {}).get("mood", {})
        if mood_data:
            note = f" — {mood_data['note']}" if mood_data.get("note") else ""
            return f"You're feeling {mood_data['mood']}{note} (as of {mood_data['time']})"
        return "No mood logged yet today."

    def get_today_summary(self):
        """Show everything that happened today."""
        today = datetime.now().strftime("%Y-%m-%d")
        data = json.loads(self.activity_file.read_text())
        today_data = data["days"].get(today, {})

        lines = [f"--- Your Day ({today}) ---"]

        mood = today_data.get("mood", {})
        if mood:
            lines.append(f"How you're feeling: {mood.get('mood', '?')} — {mood.get('note', '')}")

        working_on = today_data.get("working_on")
        if working_on:
            lines.append(f"Working on: {working_on}")

        activities = today_data.get("activities", [])
        if activities:
            lines.append("\nActivities logged:")
            for a in activities[-10:]:
                lines.append(f"  [{a['time']}] {a['text']}")

        session_history = self._read_today_log()
        if session_history:
            lines.append("\nRecent commands this session:")
            for entry in session_history[-10:]:
                lines.append(f"  {entry}")

        if len(lines) == 1:
            lines.append("Nothing tracked yet today. Tell me what you're working on!")

        return "\n".join(lines)

    def set_working_on(self, task):
        """Save what you're currently working on."""
        if not task:
            return "Tell me what you're working on!"
        today = datetime.now().strftime("%Y-%m-%d")
        data = json.loads(self.activity_file.read_text())
        if today not in data["days"]:
            data["days"][today] = {}
        data["days"][today]["working_on"] = task
        data["days"][today]["updated"] = datetime.now().isoformat()
        self.activity_file.write_text(json.dumps(data, indent=2))
        return f"Got it! I'll remember you're working on: {task}"

    def get_working_on(self):
        """Return what you're currently working on."""
        today = datetime.now().strftime("%Y-%m-%d")
        data = json.loads(self.activity_file.read_text())
        task = data["days"].get(today, {}).get("working_on")
        if task:
            return f"You're working on: {task}"
        return "You haven't told me what you're working on yet. Just say 'I'm working on [thing]'!"

    def log_activity(self, activity):
        """Log a manual activity entry."""
        if not activity:
            return "What activity should I log?"
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M")
        data = json.loads(self.activity_file.read_text())
        if today not in data["days"]:
            data["days"][today] = {}
        if "activities" not in data["days"][today]:
            data["days"][today]["activities"] = []
        data["days"][today]["activities"].append({"time": now, "text": activity})
        self.activity_file.write_text(json.dumps(data, indent=2))
        return f"Logged: {activity}"

    def get_session_history(self):
        """Read command history from today's log file."""
        entries = self._read_today_log()
        if not entries:
            return "No session history found for today."
        result = "Session history today:\n"
        for e in entries:
            result += f"  {e}\n"
        return result.strip()

    def _read_today_log(self):
        """Parse today's log file for user commands and assistant responses."""
        today = datetime.now().strftime("%Y%m%d")
        log_file = self.logs_dir / f"actions_{today}.log"
        if not log_file.exists():
            return []

        entries = []
        try:
            for line in log_file.read_text(encoding="utf-8", errors="replace").splitlines():
                if "Text input:" in line or "Executing skill:" in line or "Processing:" in line:
                    # Extract the useful part after the module name
                    parts = line.split(" - ", 3)
                    if len(parts) >= 4:
                        entries.append(f"{parts[0][:16]} | {parts[3]}")
                    elif len(parts) >= 2:
                        entries.append(line.strip())
        except Exception:
            pass
        return entries
