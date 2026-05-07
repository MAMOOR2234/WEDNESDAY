"""Google Maps skill for Wednesday."""
import sys
import webbrowser
import urllib.parse

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "Maps"
    description = "Open Google Maps for a location or get directions"

    def execute(self, args):
        location = args.get("location", "").strip()
        origin   = args.get("from", "").strip()
        dest     = args.get("to", "").strip()

        if origin and dest:
            url = (
                f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}/"
                f"{urllib.parse.quote(dest)}"
            )
            webbrowser.open(url)
            return f"Getting directions from {origin} to {dest}"

        if location:
            url = f"https://www.google.com/maps/search/{urllib.parse.quote(location)}"
            webbrowser.open(url)
            return f"Opening Maps for: {location}"

        webbrowser.open("https://maps.google.com")
        return "Opening Google Maps"
