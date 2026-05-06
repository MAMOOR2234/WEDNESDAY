#!/usr/bin/env python3
"""
Setup script for Wednesday AI Assistant
Handles first-time setup and dependency installation
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    print("\n" + "=" * 60)
    print("  Wednesday AI Assistant - Setup")
    print("=" * 60 + "\n")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)

    print("✓ Python version OK\n")

    # Create directories
    print("Creating directories...")
    Path("logs").mkdir(exist_ok=True)
    Path("assistant_workspace").mkdir(exist_ok=True)
    print("✓ Directories created\n")

    # Check .env file
    if not Path(".env").exists():
        print("⚠️ .env file not found")
        print("Copying from .env.example...\n")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✓ .env created (please edit with your API key)\n")
        else:
            print("❌ .env.example not found\n")
            sys.exit(1)

    # Install dependencies
    print("Installing dependencies...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True
    )

    if result.returncode == 0:
        print("✓ Dependencies installed\n")
    else:
        print("⚠️ Some dependencies failed to install")
        print("Manual install: pip install -r requirements.txt\n")

    # Final checks
    print("=" * 60)
    print("Setup Complete! Next steps:\n")
    print("1. Edit .env and add your GEMINI_API_KEY")
    print("   Get from: https://makersuite.google.com/app/apikeys\n")
    print("2. Run Wednesday:")
    print("   python main.py\n")
    print("3. Or use the batch script:")
    print("   run.bat\n")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
