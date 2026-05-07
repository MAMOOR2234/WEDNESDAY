"""Dictionary skill for Wednesday — word definitions with fuzzy matching."""
import sys
from difflib import get_close_matches

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill

COMMON_WORDS = {
    "ephemeral": "Lasting for a very short time.",
    "serendipity": "The occurrence of events by chance in a happy way.",
    "ubiquitous": "Present, appearing, or found everywhere.",
    "melancholy": "A feeling of pensive sadness, typically with no obvious cause.",
    "eloquent": "Fluent or persuasive in speaking or writing.",
    "ambiguous": "Open to more than one interpretation; not having one obvious meaning.",
    "resilient": "Able to withstand or recover quickly from difficult conditions.",
    "pragmatic": "Dealing with things sensibly and realistically.",
    "diligent": "Having or showing care and conscientiousness in one's work.",
    "candid": "Truthful and straightforward; frank.",
}


class Skill(BaseSkill):
    name = "Dictionary"
    description = "Look up word definitions with smart spell-check suggestions"

    def execute(self, args):
        word = args.get("word", "").strip().lower()
        if not word:
            return "What word do you want to look up?"

        # Try PyDictionary first (rich definitions)
        try:
            from PyDictionary import PyDictionary
            d = PyDictionary(word)
            meaning = d.getMeanings()
            if meaning:
                parts = []
                for pos, defs in meaning.items():
                    top = defs[0] if isinstance(defs, list) else str(defs)
                    parts.append(f"{pos}: {top}")
                return f"{word.capitalize()} — " + " | ".join(parts[:3])
        except Exception:
            pass

        # Fallback: local word list with fuzzy matching
        if word in COMMON_WORDS:
            return f"{word.capitalize()}: {COMMON_WORDS[word]}"

        suggestions = get_close_matches(word, COMMON_WORDS.keys(), n=1, cutoff=0.7)
        if suggestions:
            s = suggestions[0]
            return f"Did you mean '{s}'? — {COMMON_WORDS[s]}"

        return f"No definition found for '{word}'. Check the spelling and try again."
