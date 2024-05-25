"""
Configuration module for the bot status checker.

This module loads environment variables required for the bot to function,
such as bot token, API ID and API HASH.
It also sets up the necessary configuration settings.
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    