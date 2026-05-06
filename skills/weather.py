"""Weather skill for Wednesday - get weather info."""

import sys
import json
from urllib import request, parse

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Get weather information."""

    name = "Weather"
    description = "Get weather info for a location"

    def execute(self, args):
        """Execute weather query."""
        location = args.get("location", "current")

        if location == "current":
            return self._get_current_weather()
        else:
            return self._get_weather(location)

    def _get_current_weather(self):
        """Get current weather (based on IP)."""
        try:
            # Using wttr.in API - no key needed
            url = "https://wttr.in/?format=j1"
            with request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())

            current = data["current_condition"][0]
            temp = current["temp_C"]
            condition = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]

            return f"It's {temp}°C with {condition}. Humidity: {humidity}%"
        except Exception as e:
            return f"Weather unavailable: {e}"

    def _get_weather(self, location):
        """Get weather for specific location."""
        try:
            url = f"https://wttr.in/{location}?format=j1"
            with request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())

            current = data["current_condition"][0]
            temp = current["temp_C"]
            condition = current["weatherDesc"][0]["value"]

            return f"Weather in {location}: {temp}°C, {condition}"
        except Exception as e:
            return f"Couldn't find weather for {location}: {e}"
