"""Configuration management for UI Agent."""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration manager for UI Agent."""

    def __init__(self):
        """Initialize configuration, loading from .env if available."""
        # Try to load .env from current directory and parent directories
        env_file = self._find_env_file()
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()
        self.default_delay = float(os.getenv("DEFAULT_DELAY", "2.0"))
        self.max_task_steps = int(os.getenv("MAX_TASK_STEPS", "12"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.screen_privacy = os.getenv("SCREEN_PRIVACY", "0").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    def _find_env_file(self) -> Optional[Path]:
        """Find .env file in current or parent directories."""
        current = Path.cwd()
        for _ in range(5):  # Search up to 5 levels
            env_file = current / ".env"
            if env_file.exists():
                return env_file
            if current.parent == current:  # Reached root
                break
            current = current.parent
        return None

    def validate_api_key(self) -> bool:
        """Validate that API key is configured."""
        return bool(self.gemini_api_key)

    def get_api_key(self) -> str:
        """Get API key or raise error if not configured."""
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not configured. "
                "Set it in .env file or GEMINI_API_KEY environment variable. "
                "Get free API key from: https://makersuite.google.com/app/apikey"
            )
        return self.gemini_api_key
