"""Application control skill for Wednesday."""

import subprocess
from pathlib import Path
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Open and close applications."""

    name = "App Control"
    description = "Open or close Windows applications"

    APP_PATHS = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "paint": "C:\\Windows\\System32\\mspaint.exe",
        "outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
        "onenote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "gmail": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        
    }

    def execute(self, args):
        """Execute app control command."""
        action = args.get("action", "open")
        app_name = args.get("app_name", "").lower()

        if not app_name:
            return "No app specified"

        if action == "open":
            return self._open_app(app_name)
        elif action == "close":
            return self._close_app(app_name)
        else:
            return f"Unknown action: {action}"

    def _open_app(self, app_name):
        """Open an application."""
        if app_name in self.APP_PATHS:
            app_path = self.APP_PATHS[app_name]
            if Path(app_path).exists():
                try:
                    subprocess.Popen(app_path)
                    return f"Opening {app_name}..."
                except Exception as e:
                    return f"Failed to open {app_name}: {e}"

        try:
            subprocess.Popen(f"start {app_name}", shell=True)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    def _close_app(self, app_name):
        """Close an application."""
        try:
            subprocess.run(f"taskkill /IM {app_name}.exe /F", shell=True, capture_output=True)
            return f"Closed {app_name}"
        except Exception as e:
            return f"Failed to close {app_name}: {e}"
