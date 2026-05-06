"""Web operations skill for Wednesday - search and browsing."""

import webbrowser
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Web search and website opening."""

    name = "Web Operations"
    description = "Search the web and open websites"

    def execute(self, args):
        """Execute web operation."""
        action = args.get("action", "search")

        if action == "search":
            query = args.get("query", "")
            if not query:
                return "No search query specified"
            return self._search(query)

        elif action == "open":
            url = args.get("url", "")
            if not url:
                return "No URL specified"
            return self._open_website(url)

        else:
            return f"Unknown action: {action}"

    def _search(self, query):
        """Perform web search."""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for '{query}'..."
        except Exception as e:
            return f"Search failed: {e}"

    def _open_website(self, url):
        """Open a website."""
        try:
            if not url.startswith(("http://", "https://", "ftp://")):
                url = "https://" + url

            webbrowser.open(url)
            return f"Opening {url}..."
        except Exception as e:
            return f"Failed to open {url}: {e}"
