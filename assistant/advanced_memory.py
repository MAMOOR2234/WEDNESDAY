"""
Enhanced Persistent Memory with User Preferences
Based on Mark-XXX's memory system
"""

import json
from pathlib import Path
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)


class EnhancedMemory:
    """Enhanced memory with persistent storage and preferences."""

    def __init__(self):
        """Initialize enhanced memory system."""
        self.workspace = Path(__file__).parent.parent / "assistant_workspace"
        self.memory_file = self.workspace / "memory.json"
        self.preferences_file = self.workspace / "preferences.json"

        self.conversation = []
        self.preferences = {}
        self.user_profile = {}

        self._load_memory()
        self._load_preferences()

    def _load_memory(self):
        """Load conversation history from disk."""
        try:
            if self.memory_file.exists():
                data = json.loads(self.memory_file.read_text())
                self.conversation = data.get("conversation", [])
                self.user_profile = data.get("user_profile", {})
                logger.info(f"Loaded {len(self.conversation)} messages from memory")
        except Exception as e:
            logger.warning(f"Failed to load memory: {e}")

    def _load_preferences(self):
        """Load user preferences from disk."""
        try:
            if self.preferences_file.exists():
                raw = json.loads(self.preferences_file.read_text())
                # Handle old format that wrapped in {"preferences": {...}}
                if "preferences" in raw and isinstance(raw["preferences"], dict):
                    self.preferences = raw["preferences"]
                else:
                    self.preferences = raw
                logger.info(f"Loaded preferences: {list(self.preferences.keys())}")
        except Exception as e:
            logger.warning(f"Failed to load preferences: {e}")

    def save(self):
        """Save memory to disk."""
        try:
            memory_data = {
                "conversation": self.conversation[-50:],
                "user_profile": self.user_profile,
                "timestamp": datetime.now().isoformat()
            }
            self.memory_file.write_text(json.dumps(memory_data, indent=2))
            # Save preferences as a flat dict (no nesting)
            self.preferences_file.write_text(json.dumps(self.preferences, indent=2))
            logger.debug("Memory saved to disk")
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def add_message(self, role, content):
        """Add message to conversation."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation.append(message)
        self.save()

    def set_preference(self, key, value):
        """Set user preference."""
        self.preferences[key] = value
        self.save()
        logger.info(f"Preference set: {key} = {value}")

    def get_preference(self, key, default=None):
        """Get user preference."""
        return self.preferences.get(key, default)

    def set_user_info(self, key, value):
        """Set user profile info."""
        self.user_profile[key] = value
        self.save()

    def get_user_info(self, key, default=None):
        """Get user profile info."""
        return self.user_profile.get(key, default)

    def get_context(self):
        """Get conversation context."""
        context = []
        for msg in self.conversation[-20:]:  # Last 20 messages
            context.append(f"{msg['role'].upper()}: {msg['content']}")
        return "\n".join(context)

    def set_mood(self, mood, note=""):
        """Save how the user is currently feeling."""
        entry = {
            "mood": mood,
            "note": note,
            "timestamp": datetime.now().isoformat()
        }
        self.user_profile["current_mood"] = entry
        if "mood_history" not in self.user_profile:
            self.user_profile["mood_history"] = []
        self.user_profile["mood_history"].append(entry)
        self.user_profile["mood_history"] = self.user_profile["mood_history"][-20:]
        self.save()
        logger.info(f"Mood saved: {mood}")

    def get_mood(self):
        """Get current mood."""
        return self.user_profile.get("current_mood", {})

    def get_summary(self):
        """Get memory summary."""
        mood = self.user_profile.get("current_mood", {})
        return {
            "messages": len(self.conversation),
            "preferences": len(self.preferences),
            "user_info_fields": len(self.user_profile),
            "current_mood": mood.get("mood", "unknown"),
            "last_updated": self.conversation[-1]["timestamp"] if self.conversation else None
        }
