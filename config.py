import os

class Config:

    API_ID = int(os.environ.get("API_ID", 1))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
