"""Standalone TTS helper — reads text from stdin, speaks it.
Honors voice preference from assistant_workspace/voice_pref.txt (male/female)."""
import sys
import os
from pathlib import Path
import pyttsx3

text = sys.stdin.read().strip()
if not text:
    sys.exit(0)

# Read voice preference
pref_file = Path(__file__).parent / "assistant_workspace" / "voice_pref.txt"
voice_pref = "female"
if pref_file.exists():
    try:
        voice_pref = pref_file.read_text(encoding="utf-8").strip() or "female"
    except Exception:
        pass

engine = pyttsx3.init()
engine.setProperty("rate", 165)

voices = engine.getProperty("voices")
if len(voices) > 1:
    # On Windows: voices[0] is typically male (David), voices[1] is female (Zira)
    target_idx = 1 if voice_pref == "female" else 0
    target_idx = min(target_idx, len(voices) - 1)
    engine.setProperty("voice", voices[target_idx].id)

engine.say(text)
engine.runAndWait()
