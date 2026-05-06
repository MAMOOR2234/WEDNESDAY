"""
Wednesday AI Assistant - Enhanced with JARVIS-style Architecture
Core Engine Orchestrator
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

from assistant.brain import WednesdayBrain
from assistant.advanced_memory import EnhancedMemory
from assistant.config import Config
from assistant.skills_registry import SkillsRegistry
from assistant.logger import setup_logger

logger = setup_logger(__name__)


class WednesdayCore:
    """Core orchestrator for Wednesday AI - handles skill execution and reasoning."""

    def __init__(self):
        """Initialize Wednesday core engine."""
        self.config = Config()
        self.memory = EnhancedMemory()
        self.skills = SkillsRegistry()

        # Initialize brain based on config
        if self.config.brain_type == "claude":
            from .claude_brain import ClaudeBrain
            self.brain = ClaudeBrain()
            logger.info("Using Claude brain")
        elif self.config.brain_type == "openai":
            from .openai_brain import OpenAIBrain
            self.brain = OpenAIBrain()
            logger.info("Using OpenAI brain")
        else:
            self.brain = WednesdayBrain()
            logger.info("Using Gemini brain")

        logger.info("Wednesday Core Engine initialized")
        print("[*] Wednesday Core Engine Ready")

    def process_input(self, user_input):
        """Process user input and execute appropriate skill."""
        if not user_input:
            return None, []

        # Add to memory
        self.memory.add_message("user", user_input)

        # Fast path for explicit OpenClaw commands.
        shortcut_skill = self._match_openclaw_shortcut(user_input)
        if shortcut_skill:
            skill_result = self.execute_skill(shortcut_skill)
            response = "Done. OpenClaw command executed."
            self.memory.add_message("assistant", response)
            return response, [skill_result]

        # Get AI response and skill recommendations
        logger.info(f"Processing: {user_input[:50]}...")
        project_context = self._get_project_context()
        response, skills_to_execute = self.brain.process(
            user_input,
            self.memory.get_context(),
            project_context
        )

        # Execute skills
        skill_results = []
        for skill_call in skills_to_execute:
            result = self.execute_skill(skill_call)
            skill_results.append(result)

        # Add response to memory
        self.memory.add_message("assistant", response)

        return response, skill_results

    def execute_skill(self, skill_call):
        """Execute a skill with safety confirmation."""
        skill_name = skill_call.get("name") or skill_call.get("skill") or "unknown"
        args = dict(skill_call.get("args", {}))
        action = skill_call.get("action")
        if action and "action" not in args:
            args["action"] = action

        logger.info(f"Executing skill: {skill_name}")

        try:
            result = self.skills.execute(skill_name, args)
            return {
                "skill": skill_name,
                "status": "success",
                "result": result
            }
        except Exception as e:
            logger.error(f"Skill execution error - {skill_name}: {e}")
            return {
                "skill": skill_name,
                "status": "error",
                "error": str(e)
            }

    def _match_openclaw_shortcut(self, user_input):
        """Map direct OpenClaw user commands to skill calls."""
        text = user_input.strip()
        lowered = text.lower()

        if lowered in {"openclaw", "openclaw status", "openclaw health"}:
            return {"name": "openclaw", "args": {"action": "status"}}

        if lowered in {"openclaw info", "openclaw gateway info"}:
            return {"name": "openclaw", "args": {"action": "info"}}

        match = re.match(r"^openclaw\s+search\s+(.+)$", text, flags=re.IGNORECASE)
        if match:
            return {
                "name": "openclaw",
                "args": {
                    "action": "search",
                    "query": match.group(1).strip(),
                },
            }

        match = re.match(r"^openclaw\s+fetch\s+(.+)$", text, flags=re.IGNORECASE)
        if match:
            return {
                "name": "openclaw",
                "args": {
                    "action": "fetch",
                    "url": match.group(1).strip(),
                },
            }

        match = re.match(r"^openclaw\s+send\s+to\s+(.+?)\s*:\s*(.+)$", text, flags=re.IGNORECASE)
        if match:
            return {
                "name": "openclaw",
                "args": {
                    "action": "send",
                    "target": match.group(1).strip(),
                    "message": match.group(2).strip(),
                },
            }

        match = re.match(r"^openclaw\s+send\s+(.+)$", text, flags=re.IGNORECASE)
        if match:
            return {
                "name": "openclaw",
                "args": {
                    "action": "send",
                    "message": match.group(1).strip(),
                },
            }

        return None

    def _get_project_context(self):
        """Return loaded project context string if any project is loaded."""
        try:
            return self.skills.execute("code_assistant", {"action": "get_context"})
        except Exception:
            return ""

    def get_available_skills(self):
        """Get list of available skills."""
        return self.skills.list_skills()

    def get_conversation_context(self):
        """Get current conversation context."""
        return self.memory.get_messages()
