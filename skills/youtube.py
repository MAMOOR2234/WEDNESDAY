"""YouTube skill for Wednesday — search, open, download."""
import sys
import webbrowser
import urllib.parse

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "YouTube"
    description = "Search YouTube, open videos, or download videos"

    def execute(self, args):
        action = args.get("action", "search")
        query  = args.get("query", "").strip()
        url    = args.get("url", "").strip()

        if action == "open":
            webbrowser.open("https://youtube.com")
            return "Opening YouTube..."

        elif action == "search":
            if not query:
                return "What do you want to search on YouTube?"
            encoded = urllib.parse.quote(query)
            webbrowser.open(f"https://www.youtube.com/results?search_query={encoded}")
            return f"Searching YouTube for: {query}"

        elif action == "download":
            target = url or query
            if not target:
                return "Provide a YouTube URL to download"
            try:
                import subprocess
                result = subprocess.run(
                    [sys.executable, "-m", "yt_dlp", target, "-o", "%(title)s.%(ext)s"],
                    capture_output=True, text=True, timeout=120
                )
                if result.returncode == 0:
                    return f"Downloaded: {target}"
                return f"Download failed: {result.stderr[:200]}"
            except FileNotFoundError:
                return "yt-dlp not installed. Run: pip install yt-dlp"
            except Exception as e:
                return f"Download error: {e}"

        return f"Unknown YouTube action: {action}"
