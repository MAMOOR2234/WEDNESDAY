"""News skill - fetch top headlines from RSS."""

import sys
import json
from urllib import request
from datetime import datetime

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "News"
    description = "Fetch top news headlines"

    FEEDS = {
        "tech":    "https://feeds.feedburner.com/TechCrunch",
        "world":   "https://feeds.bbci.co.uk/news/world/rss.xml",
        "science": "https://www.sciencedaily.com/rss/top/science.xml",
        "default": "https://feeds.bbci.co.uk/news/rss.xml",
    }

    def execute(self, args):
        category = args.get("category", "default").lower()
        count = int(args.get("count", 5))
        url = self.FEEDS.get(category, self.FEEDS["default"])
        return self._fetch(url, count, category)

    def _fetch(self, url, count, category):
        try:
            req = request.Request(url, headers={"User-Agent": "Wednesday/1.0"})
            with request.urlopen(req, timeout=8) as r:
                content = r.read().decode("utf-8", errors="replace")

            import re
            titles = re.findall(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", content)
            # skip first title (feed name)
            headlines = [t.strip() for t in titles[1:count+1] if t.strip()]

            if not headlines:
                return "No headlines found."

            label = category.upper() if category != "default" else "TOP"
            result = f"// {label} NEWS //\n"
            for i, h in enumerate(headlines, 1):
                result += f"{i}. {h}\n"
            return result.strip()
        
        def _parse_date(self, date_str):
            try:
                return self.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                return "error parsing date"

        except Exception as e:
            return f"News fetch failed: {e}"
