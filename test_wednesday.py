"""Quick end-to-end test for Wednesday."""
import os
os.environ["PYTHONUTF8"] = "1"

from assistant.core import WednesdayCore

core = WednesdayCore()
print("=== Wednesday is LIVE ===\n")

tests = [
    "yo whats up!",
    "what time is it?",
    "how is my computer doing?",
    "what did i do today and what am i working on?",
]

for msg in tests:
    print(f"You: {msg}")
    response, skill_results = core.process_input(msg)
    print(f"Wednesday: {response}")
    if skill_results:
        for r in skill_results:
            label = r["skill"]
            detail = str(r.get("result", r.get("error", "")))[:150]
            print(f"  [{label}] -> {detail}")
    print()
