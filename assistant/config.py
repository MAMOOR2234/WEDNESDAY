"""Configuration management for Wednesday assistant."""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration settings for Wednesday."""

    def __init__(self):
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)

        self.brain_type = os.getenv("BRAIN_TYPE", "claude").lower()

        # Claude (Anthropic) — default brain
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.claude_model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

        # OpenAI — fallback option
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Speech settings
        self.speech_language = os.getenv("SPEECH_LANGUAGE", "en-US")
        self.speech_timeout = int(os.getenv("SPEECH_TIMEOUT", "10"))
        self.speech_engine = os.getenv("SPEECH_ENGINE", "speech_recognition")

        # TTS settings
        self.tts_engine = os.getenv("TTS_ENGINE", "pyttsx3")
        self.tts_speed = int(os.getenv("TTS_SPEED", "150"))
        self.tts_voice = os.getenv("TTS_VOICE", "default")

        # Workspace
        self.workspace_dir = Path(__file__).parent.parent / "assistant_workspace"
        self.workspace_dir.mkdir(exist_ok=True)

        self._validate()

    def _validate(self):
        if self.brain_type == "claude":
            if not self.anthropic_api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not set. Add it to your .env file."
                )
        elif self.brain_type == "openai":
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY not set. Add it to your .env file."
                )
        else:
            raise ValueError(
                f"Invalid BRAIN_TYPE: '{self.brain_type}'. Use 'claude' or 'openai'."
            )
