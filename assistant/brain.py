"""Gemini brain for Wednesday assistant."""

import json
import re
from .config import Config
from .logger import setup_logger

logger = setup_logger(__name__)


class WednesdayBrain:
    """Gemini-powered reasoning engine for Wednesday."""

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

RESPONSE EXAMPLES (what NOT to do):
❌ "I will proceed to open Chrome for you."
✅ "Yo, opening Chrome now!"

❌ "The current time is 3:47 PM"
✅ "It's like 3:47 PM right now, why, you late for something? 😂"

❌ "I can assist you with web searches."
✅ "Yeah bro, I got you. Let me find that for you real quick."

TONE:
- Friendly and relatable
- Like texting a close friend
- Not corporate or formal
- A bit playful
- Show that you actually care
- Can tease back if they're joking

AVAILABLE SKILLS:
You can help with:
1. app_control - Open/close apps (Chrome, Word, etc.)
2. web_operations - Search the web, open websites
3. file_operations - Save/read files
4. keyboard_control - Type text for you
5. information - Time, date, system info
6. openclaw - Talk to the local OpenClaw gateway and check its status
7. daily_tracker - See what you did today, what you're working on, log activities
   - action: "summary" → show everything from today
   - action: "set_working_on", task: "..." → remember what they're working on
   - action: "get_working_on" → what are they working on
   - action: "log_activity", activity: "..." → log a task/activity
   - action: "history" → today's session command history
8. reminders_notes - Create reminders and notes
9. weather - Get weather info
10. system_info - Monitor system stats

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

REMEMBER:
- You're friends, not boss-employee
- Keep responses short and punchy (like texts)
- Be real and genuine
- Show personality in everything
- Make them feel understood
- Have fun with it!"""

    def __init__(self):
        """Initialize Gemini brain."""
        self.config = Config()
        self.client = self._init_client()
        logger.info("Wednesday brain initialized with Gemini")

    def _init_client(self):
        """Initialize Gemini client using google-genai SDK."""
        try:
            from google import genai
            client = genai.Client(api_key=self.config.gemini_api_key)
            return client
        except ImportError:
            logger.error("google-genai not installed")
            raise ImportError("Please install: pip install google-genai")

    def process(self, user_input, conversation_context=""):
        """Process user input and return response with potential tool calls."""
        try:
            full_prompt = self._build_prompt(user_input, conversation_context)

            response = self.client.models.generate_content(
                model=self.config.gemini_model,
                contents=full_prompt,
            )

            response_text = response.text
            tools = self._extract_tool_calls(response_text)

            # Clean up response text (remove tool_calls section)
            clean_response = self._clean_response(response_text)

            logger.info(f"Gemini response: {clean_response[:100]}...")
            if tools:
                logger.info(f"Extracted {len(tools)} tool calls")

            return clean_response, tools

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            error_response = f"I encountered an error: {str(e)}. Please check your API key and internet connection."
            return error_response, []

    def _build_prompt(self, user_input, context):
        """Build the full prompt for Gemini."""
        prompt = f"{self.SYSTEM_PROMPT}\n\n"

        if context:
            prompt += f"RECENT CONVERSATION:\n{context}\n\n"

        prompt += f"USER REQUEST: {user_input}"

        return prompt

    def _extract_tool_calls(self, response_text):
        """Extract skill calls from response."""
        tools = []
        try:
            # Find <skills> section
            match = re.search(r'<skills>(.*?)</skills>', response_text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                # Handle multiple JSON objects
                json_objects = re.findall(r'\{[^{}]*\}', json_str)
                for json_obj in json_objects:
                    tool = json.loads(json_obj)
                    tools.append(tool)
                    logger.debug(f"Extracted skill: {tool}")
        except Exception as e:
            logger.warning(f"Skill extraction error: {e}")

        return tools

    def _clean_response(self, response_text):
        """Remove skills section from response."""
        clean = re.sub(r'<skills>.*?</skills>', '', response_text, flags=re.DOTALL)
        return clean.strip()
