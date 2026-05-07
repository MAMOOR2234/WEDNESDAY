"""Joke skill for Wednesday."""
import sys
if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    name = "Jokes"
    description = "Tell a random joke"

    def execute(self, args):
        category = args.get("category", "neutral")
        try:
            import pyjokes
            joke = pyjokes.get_joke(language="en", category=category)
            return joke
        except Exception:
            import random
            fallbacks = [
                "Why don't scientists trust atoms? Because they make up everything.",
                "I told my computer I needed a break. Now it won't stop sending me KitKat ads.",
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "I would tell you a UDP joke but you might not get it.",
            ]
            return random.choice(fallbacks)
