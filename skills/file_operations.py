"""File operations skill for Wednesday - safe file I/O."""

from pathlib import Path
from assistant.config import Config
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Safe file read/write operations."""

    name = "File Operations"
    description = "Read and write files safely in workspace"

    def __init__(self):
        """Initialize file skill."""
        self.config = Config()
        self.workspace = self.config.workspace_dir

    def execute(self, args):
        """Execute file operation."""
        action = args.get("action", "read")
        filename = args.get("filename", "")

        if not filename:
            return "Filename required"

        if action == "read":
            return self._read_file(filename)
        elif action == "write":
            content = args.get("content", "")
            return self._write_file(filename, content)
        else:
            return f"Unknown action: {action}"

    def _read_file(self, filename):
        """Read a file from workspace."""
        file_path = self.workspace / filename
        file_path = file_path.resolve()

        # Security: prevent directory traversal
        if not str(file_path).startswith(str(self.workspace)):
            return "File read denied - must be in workspace"

        try:
            if not file_path.exists():
                return f"File not found: {filename}"

            content = file_path.read_text(encoding="utf-8")
            return content
        except Exception as e:
            return f"File read error: {e}"

    def _write_file(self, filename, content):
        """Write a file to workspace."""
        file_path = self.workspace / filename
        file_path = file_path.resolve()

        # Security: prevent directory traversal
        if not str(file_path).startswith(str(self.workspace)):
            return "File write denied - must be in workspace"

        try:
            file_path.write_text(content, encoding="utf-8")
            return f"Saved to {filename}"
        except Exception as e:
            return f"File write error: {e}"
