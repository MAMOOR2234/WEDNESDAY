"""Wikipedia search skill for Wednesday."""
import sys
if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "Wikipedia"
    description = "Search Wikipedia for information on any topic"

    def execute(self, args):
        query = args.get("query", "").strip()
        sentences = int(args.get("sentences", 2))
        if not query:
            return "What do you want to look up on Wikipedia?"
        try:
            import wikipedia
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
            return f"According to Wikipedia: {result}"
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:4])
            return f"Too many results — did you mean: {options}?"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query}'"
        except Exception as e:
            return f"Wikipedia error: {e}"
