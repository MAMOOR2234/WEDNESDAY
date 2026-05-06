"""Information skill for Wednesday - time, date, system info."""

from datetime import datetime
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Get system and time information."""

    name = "Information"
    description = "Get time, date, and system information"

    def execute(self, args):
        """Execute information query."""
        query_type = args.get("type", "time")

        if query_type == "time":
            return self._get_time()
        elif query_type == "date":
            return self._get_date()
        elif query_type == "datetime":
            return self._get_datetime()
        else:
            return f"Unknown query type: {query_type}"

    def _get_time(self):
        """Get current time."""
        return datetime.now().strftime("%I:%M %p")

    def _get_date(self):
        """Get current date."""
        return datetime.now().strftime("%A, %B %d, %Y")

    def _get_datetime(self):
        """Get current date and time."""
        return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
