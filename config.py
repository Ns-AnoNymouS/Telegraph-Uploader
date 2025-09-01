"""
Configuration module for the Telegraph uploader.

This module handles loading and validating environment variables required
for the bot to function, such as API credentials, tokens, and domain settings.
"""

import sys
import logging
from os import getenv
from dotenv import load_dotenv

# Configure logger for this module
logger = logging.getLogger(__name__)
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    API_ID: int = int(getenv("API_ID", "0"))
    API_HASH: str | None = getenv("API_HASH")
    BOT_TOKEN: str | None = getenv("BOT_TOKEN")
    DOMAIN: str = getenv("DOMAIN", "graph.org")
    # Optional: API key for image uploads (https://api.imgbb.com/)
    IMGBB_API_KEY: str | None = getenv("IMGBB_API_KEY")

    @classmethod
    def validate(cls):
        """Validate required configuration and exit if invalid."""
        missing = []

        if cls.API_ID == 0:
            missing.append("API_ID")

        if not cls.API_HASH:
            missing.append("API_HASH")

        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")

        if missing:
            logger.critical("Missing required configuration: %s", ", ".join(missing))
            sys.exit(1)

        if not cls.IMGBB_API_KEY:
            logger.warning(
                "No IMGBB_API_KEY found. Falling back to envs.sh for photo upload."
            )
