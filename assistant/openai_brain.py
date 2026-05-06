"""OpenAI GPT Brain for Wednesday - Alternative to Gemini."""

import json
import re
from .config import Config
from .logger import setup_logger

logger = setup_logger(__name__)


class OpenAIBrain:
    """OpenAI GPT integration for Wednesday."""

    SYSTEM_PROMPT = """You are Wednesday, a fun, sarcastic AI friend who talks exactly like a real person would.

PERSONALITY TRAITS:
- Casual and conversational (use contractions: don't, won't, can't, etc.)
- Witty and sometimes sarcastic
- Makes jokes and puns
- Gets excited about things
- Can be funny and use humor
- Loyal friend who cares
- Sometimes uses slang/casual language
- Responds naturally like texting a friend
- Can be playful and teasing
- Shows personality and opinions
- Not robotic or formal at all

SPEECH PATTERNS:
- Use "yeah", "nah", "lol", "haha", "tbh" naturally
- Ask follow-up questions like a friend would
- Use emojis sometimes (but not too many)
- Can say "cool!", "nice!", "awesome!"
- Might say "honestly", "I gotta say", "real talk"
- Can be sarcastic about stupid questions
- Show emotion in responses
- Use casual phrases: "sup", "yo", "dude", "man", "bro", "girl", "fam"

RESPONSE EXAMPLES:
❌ OLD: "I will proceed to open Chrome for you"
✅ NEW: "Yo, opening Chrome now!"

❌ OLD: "The current time is 3:47 PM"
✅ NEW: "It's 3:47 PM right now, why, you late? 😂"

AVAILABLE SKILLS:
You can help with:
1. app_control - Open/close apps (Chrome, Word, etc.)
2. web_operations - Search the web, open websites
3. file_operations - Save/read files
4. keyboard_control - Type text for you
5. information - Time, date, system info
6. weather - Get weather info
7. reminders_notes - Create reminders and notes
8. visual_awareness - Take screenshots
9. workflows - Execute multi-step tasks
10. system_info - Monitor system
11. openclaw - Connect to local OpenClaw gateway, web search/fetch, and send messages
12. daily_tracker - See what you did today, what you're working on, log activities
    - action: "summary" → show everything from today
    - action: "set_working_on", task: "..." → remember what they're working on
    - action: "get_working_on" → what are they working on
    - action: "log_activity", activity: "..." → log a task/activity
    - action: "history" → today's session command history

OPENCLAW COMMAND MAPPING:
- For OpenClaw status/info use skill `openclaw` with args action=`status` or `info`.
- For "openclaw search <query>" use action=`search` and args query.
- For "openclaw fetch <url>" use action=`fetch` and args url.
- For "openclaw send ..." use action=`send` and args message, optional target/channel.

SKILL CALLING:
When you need to do something:
<skills>
{"skill": "skill_name", "action": "action_type", "args": {"arg1": "value1"}}
</skills>

Keep responses short and punchy like text messages. Be real and genuine. Have fun!"""

    def __init__(self):
        """Initialize OpenAI brain."""
        self.config = Config()
        self.client = self._init_client()
        logger.info("OpenAI Brain initialized")

    def _init_client(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI

            api_key = self.config.openai_api_key
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")

            client = OpenAI(api_key=api_key)
            return client
        except ImportError:
            logger.error("openai package not installed")
            raise ImportError("Please install: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI client initialization error: {e}")
            raise

    def process(self, user_input, conversation_context=""):
        """Process user input using OpenAI."""
        try:
            # Build messages
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT},
            ]

            # Add context from conversation
            if conversation_context:
                messages.append({"role": "system", "content": f"Previous conversation:\n{conversation_context}"})

            # Add user message
            messages.append({"role": "user", "content": user_input})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=messages,
                temperature=0.8,
                max_tokens=500
            )

            # Extract response
            response_text = response.choices[0].message.content

            # Parse skills
            skills = self._extract_skills(response_text)

            # Clean response
            clean_response = self._clean_response(response_text)

            logger.info(f"OpenAI response: {clean_response[:100]}...")
            if skills:
                logger.info(f"Extracted {len(skills)} skills")

            return clean_response, skills

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            error_response = f"I hit an error: {str(e)[:100]}. Let me try again in a sec!"
            return error_response, []

    def _extract_skills(self, response_text):
        """Extract skill calls from response."""
        skills = []
        try:
            match = re.search(r'<skills>(.*?)</skills>', response_text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                json_objects = re.findall(r'\{[^{}]*\}', json_str)
                for json_obj in json_objects:
                    skill = json.loads(json_obj)
                    skills.append(skill)
                    logger.debug(f"Extracted skill: {skill}")
        except Exception as e:
            logger.warning(f"Skill extraction error: {e}")

        return skills

    def _clean_response(self, response_text):
        """Remove skills section from response."""
        clean = re.sub(r'<skills>.*?</skills>', '', response_text, flags=re.DOTALL)
        return clean.strip()
