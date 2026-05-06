"""Windows control tools for Wednesday assistant."""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
from .config import Config
from .logger import setup_logger

logger = setup_logger(__name__)


class WindowsTools:
    """Tools for controlling Windows and performing system actions."""

    # Common app paths for Windows
    APP_PATHS = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "notepad": "C:\\Windows\\System32\\notepad.exe",
        "calculator": "C:\\Windows\\System32\\calc.exe",
        "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
        "teams": "C:\\Program Files\\Microsoft\\Teams\\current\\Teams.exe",
        "slack": "C:\\Users\\%USERNAME%\\AppData\\Local\\Slack\\app-*\\slack.exe",
    }

    def __init__(self):
        """Initialize tools."""
        self.config = Config()

    def execute(self, tool_name, args):
        """Execute a tool action."""
        try:
            if tool_name == "open_app":
                return self.open_app(args.get("app_name"))
            elif tool_name == "close_app":
                return self.close_app(args.get("app_name"))
            elif tool_name == "open_website":
                return self.open_website(args.get("url"))
            elif tool_name == "web_search":
                return self.web_search(args.get("query"))
            elif tool_name == "type_text":
                return self.type_text(args.get("text"))
            elif tool_name == "file_write":
                return self.file_write(args.get("filename"), args.get("content"))
            elif tool_name == "file_read":
                return self.file_read(args.get("filename"))
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            logger.error(f"Tool execution error - {tool_name}: {e}")
            raise

    def open_app(self, app_name):
        """Open a Windows application."""
        if not app_name:
            return "No app specified"

        app_name_lower = app_name.lower()
        logger.info(f"Opening app: {app_name}")

        # Try to find and open the app
        if app_name_lower in self.APP_PATHS:
            app_path = self.APP_PATHS[app_name_lower]
            app_path = os.path.expandvars(app_path)

            if os.path.exists(app_path):
                try:
                    subprocess.Popen(app_path)
                    logger.info(f"Opened {app_name}")
                    return f"Opening {app_name}..."
                except Exception as e:
                    logger.error(f"Failed to open {app_name}: {e}")
                    return f"Failed to open {app_name}: {e}"

        # Try generic search
        try:
            subprocess.Popen(f"start {app_name}", shell=True)
            logger.info(f"Started {app_name}")
            return f"Opening {app_name}..."
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return f"I couldn't find {app_name}. Try being more specific."

    def close_app(self, app_name):
        """Close a Windows application."""
        if not app_name:
            return "No app specified"

        app_name_lower = app_name.lower()
        logger.info(f"Closing app: {app_name}")

        try:
            # Use taskkill to close the app
            subprocess.run(f"taskkill /IM {app_name_lower}.exe /F", shell=True, capture_output=True)
            logger.info(f"Closed {app_name}")
            return f"Closed {app_name}"
        except Exception as e:
            logger.error(f"Failed to close {app_name}: {e}")
            return f"Failed to close {app_name}: {e}"

    def open_website(self, url):
        """Open a URL in the default browser."""
        if not url:
            return "No URL specified"

        # Add protocol if missing
        if not url.startswith(("http://", "https://", "ftp://")):
            url = "https://" + url

        logger.info(f"Opening website: {url}")

        try:
            webbrowser.open(url)
            logger.info(f"Opened {url}")
            return f"Opening {url} in your browser..."
        except Exception as e:
            logger.error(f"Failed to open {url}: {e}")
            return f"Failed to open {url}: {e}"

    def web_search(self, query):
        """Perform a web search."""
        if not query:
            return "No search query specified"

        logger.info(f"Web search: {query}")

        try:
            # Use Google search URL
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            logger.info(f"Searched for: {query}")
            return f"Searching for '{query}'..."
        except Exception as e:
            logger.error(f"Search error: {e}")
            return f"Failed to search: {e}"

    def type_text(self, text):
        """Type text on the screen."""
        if not text:
            return "No text specified"

        logger.info(f"Typing text: {text[:50]}...")

        try:
            import pyautogui

            # Add delay to ensure focus
            time.sleep(1)

            # Type the text character by character (safer than paste)
            pyautogui.typewrite(text)

            logger.info(f"Typed text: {text[:50]}...")
            return f"Typed: {text[:50]}..."
        except ImportError:
            logger.error("pyautogui not installed")
            return "Text typing requires pyautogui. Install with: pip install pyautogui"
        except Exception as e:
            logger.error(f"Type text error: {e}")
            return f"Failed to type text: {e}"

    def file_write(self, filename, content):
        """Write content to a file in assistant_workspace."""
        if not filename or not content:
            return "Filename and content required"

        # Safety: ensure file is in workspace
        file_path = self.config.workspace_dir / filename
        file_path = file_path.resolve()

        # Prevent directory traversal
        if not str(file_path).startswith(str(self.config.workspace_dir)):
            logger.error(f"File write denied - outside workspace: {file_path}")
            return "File write denied - must be in assistant_workspace/"

        logger.info(f"Writing file: {filename}")

        try:
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"File written: {filename} ({len(content)} bytes)")
            return f"Saved to {filename}"
        except Exception as e:
            logger.error(f"File write error: {e}")
            return f"Failed to write file: {e}"

    def file_read(self, filename):
        """Read a file from assistant_workspace."""
        if not filename:
            return "Filename required"

        # Safety: ensure file is in workspace
        file_path = self.config.workspace_dir / filename
        file_path = file_path.resolve()

        # Prevent directory traversal
        if not str(file_path).startswith(str(self.config.workspace_dir)):
            logger.error(f"File read denied - outside workspace: {file_path}")
            return "File read denied - must be in assistant_workspace/"

        logger.info(f"Reading file: {filename}")

        try:
            if not file_path.exists():
                logger.warning(f"File not found: {filename}")
                return f"File not found: {filename}"

            content = file_path.read_text(encoding="utf-8")
            logger.info(f"File read: {filename} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"File read error: {e}")
            return f"Failed to read file: {e}"
