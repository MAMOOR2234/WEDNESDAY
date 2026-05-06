#!/usr/bin/env python3
"""
Wednesday Diagnostic Tool
Run this to check if everything is set up correctly
"""

import sys
import os
from pathlib import Path


def check_python():
    """Check Python version."""
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 8):
        print("  [FAIL] Python 3.8+ required")
        return False
    print("  [OK]")
    return True


def check_files():
    """Check project files."""
    print("\nProject files:")
    files = [
        ".env",
        "main.py",
        "requirements.txt",
        "assistant/brain.py",
        "assistant/speech.py",
        "assistant/tts.py",
        "assistant/tools.py",
        "assistant/memory.py",
        "assistant/config.py",
    ]
    all_ok = True
    for f in files:
        exists = Path(f).exists()
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {f}")
        if not exists:
            all_ok = False
    return all_ok


def check_directories():
    """Check directories."""
    print("\nDirectories:")
    dirs = ["logs", "assistant_workspace", "assistant"]
    for d in dirs:
        exists = Path(d).exists()
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {d}")
        if not exists:
            Path(d).mkdir(exist_ok=True)


def check_env():
    """Check environment variables."""
    print("\nEnvironment (.env):")
    env_path = Path(".env")

    if not env_path.exists():
        print("  [MISSING] .env file not found")
        return False

    env_content = env_path.read_text()
    checks = {
        "GEMINI_API_KEY": "Gemini API key",
        "GEMINI_MODEL": "Gemini model",
        "SPEECH_ENGINE": "Speech engine",
        "TTS_ENGINE": "TTS engine",
    }

    all_ok = True
    for key, label in checks.items():
        if key in env_content and f"{key}=" in env_content:
            value = env_content.split(f"{key}=")[1].split("\n")[0].strip()
            if value and "your_" not in value.lower():
                print(f"  [OK] {label}: {value[:30]}")
            else:
                print(f"  [FAIL] {label}: NOT SET")
                all_ok = False
        else:
            print(f"  [MISSING] {label}: MISSING")
            all_ok = False

    return all_ok


def check_dependencies():
    """Check if Python packages are installed."""
    print("\nDependencies:")
    packages = {
        "google.generativeai": "Gemini API",
        "speech_recognition": "Speech Recognition",
        "pyttsx3": "pyttsx3 TTS",
        "faster_whisper": "faster-whisper (optional)",
        "edge_tts": "edge-tts (optional)",
        "pyautogui": "pyautogui",
        "dotenv": "python-dotenv",
    }

    for package, label in packages.items():
        try:
            __import__(package)
            print(f"  [OK] {label}")
        except ImportError:
            optional = "(optional)" in label
            status = "[OPTIONAL]" if optional else "[MISSING]"
            print(f"  {status} {label}")


def check_microphone():
    """Check microphone availability."""
    print("\nMicrophone:")
    try:
        import speech_recognition as sr

        mics = sr.Microphone()
        print("  [OK] Microphone detected")
        return True
    except Exception as e:
        print(f"  [WARNING] Microphone check failed: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("  Wednesday Diagnostic Tool")
    print("=" * 60)

    check_python()
    check_files()
    check_directories()
    check_env()
    check_dependencies()
    check_microphone()

    print("\n" + "=" * 60)
    print("Diagnostic complete!")
    print("=" * 60 + "\n")

    print("Next steps:")
    print("1. Install missing dependencies: pip install -r requirements.txt")
    print("2. Edit .env and add GEMINI_API_KEY")
    print("3. Run: python main.py\n")


if __name__ == "__main__":
    main()
