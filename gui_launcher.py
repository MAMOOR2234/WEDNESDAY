#!/usr/bin/env python3
"""
Wednesday AI Assistant - GUI Mode Launcher
JARVIS-Style Interface
"""

import sys
import os

# Add assistant module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant.core import WednesdayCore
from assistant.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Launch Wednesday GUI."""
    print("[*] Initializing Wednesday Core Engine...")
    core = WednesdayCore()

    print("[*] Loading GUI Interface...")
    try:
        from assistant.gui import launch_gui
        logger.info("Launching GUI mode")
        launch_gui(core)
    except ImportError as e:
        print(f"[!] GUI dependencies missing: {e}")
        print("[*] Installing PyQt6...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
        print("[*] Retrying GUI launch...")
        from assistant.gui import launch_gui
        launch_gui(core)


if __name__ == "__main__":
    main()
