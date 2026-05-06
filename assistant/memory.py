"""Conversation memory for Wednesday assistant."""

from collections import deque
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)


class ConversationMemory:
    """Maintains short-term conversation context."""

    def __init__(self, max_messages=20):
        """Initialize memory with max message capacity."""
        self.messages = deque(maxlen=max_messages)
        self.max_messages = max_messages

    def add_message(self, role, content):
        """Add a message to memory."""
        message = {
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        logger.debug(f"Memory: {role} - {content[:50]}...")

    def get_context(self):
        """Get formatted context for Gemini."""
        context = []
        for msg in self.messages:
            context.append(f"{msg['role'].upper()}: {msg['content']}")
        return "\n".join(context)

    def get_messages(self):
        """Get all messages."""
        return list(self.messages)

    def clear(self):
        """Clear all messages."""
        self.messages.clear()
        logger.info("Memory cleared")

    def summary(self):
        """Get a summary of conversation."""
        return f"Recent messages: {len(self.messages)}/{self.max_messages}"
