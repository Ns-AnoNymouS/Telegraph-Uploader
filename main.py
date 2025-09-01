"""
Telegraph Uploader Bot

This module defines a Telegram bot that can upload photos to imgBB / envs.sh and
create instant view links for text messages.
The bot is built using the Pyrogram library and the Telegraph API.

Features:
- Upload photos to imgBB / envs.sh and return the URL.
- Create graph.org posts from text messages, with support for custom titles and emoji removal.

Classes:
- Bot: A subclass of Pyrogram's Client, representing the Telegram bot.

Functions:
- start_handlers: Handles the /start command to provide a welcome message.
- photo_handler: Handles incoming photo messages, uploads them to imgBB / envs.sh,
                 and sends the URL to the user.
- text_handler: Handles incoming text messages, creates graph.org posts,
                and sends the URL to the user.

Patterns:
- EMOJI_PATTERN: Regular expression to match <emoji> tags in the text.
- TITLE_PATTERN: Regular expression to match title lines in the text.

Usage:
1. Send a /start command to receive a welcome message.
2. Send a photo to upload it to imgBB / envs.sh and get the link.
3. Send a text message in the format
        Title: {title}
        {content}
    to create a Telegra.ph post.
"""

import logging
import logging.config

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import os
import re
import time

import requests
from telegraph import Telegraph
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from utils import progress

try:
    import uvloop  # https://docs.pyrogram.org/topics/speedups#uvloop

    uvloop.install()
except ImportError:
    pass


class Bot(Client):  # pylint: disable=too-many-ancestors
    """Telegram bot client for uploading photos and creating posts on Telegra.ph."""

    def __init__(self):
        """Initializes the bot with the provided configuration."""
        super().__init__(
            "telegraph",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
        )

    async def start(self):
        """Starts the bot and prints the bot username."""
        Config.validate()
        await super().start()
        logger.info("Bot started successfully at @%s", self.me.username)
        logger.debug("Full bot info: %s", self.me)

    async def stop(self, *args, **kwargs):
        """Stops the bot and prints a stop message."""
        await super().stop(*args, **kwargs)
        logger.info("Bot session stopped gracefully.")


bot = Bot()
EMOJI_PATTERN = re.compile(r'<emoji id="\d+">')
TITLE_PATTERN = re.compile(r"title:? (.*)", re.IGNORECASE)


@bot.on_message(filters.command("start") & filters.incoming & filters.private)
async def start_handlers(_: Bot, message: Message) -> None:
    """Handles the /start command to provide a welcome message to the user."""

    logger.debug("Recieced /start command from user %s", message.from_user.first_name)
    await message.reply(
        text=(
            f"👋 **Hello {message.from_user.mention}!**\n\n"
            "✨ Welcome to the **Telegraph Uploader Bot!**\n\n"
            "With me, you can:\n"
            "📸 **Upload Photos** → Send me any photo, and I'll upload it to **ImgBB** or **Envs.sh** with a direct shareable link.\n"
            "📝 **Create Instant View Posts** → Send me text in a simple format, and I’ll create a stylish post on **Graph.org** (Telegraph alternative).\n\n"
            "📌 **Usage**:\n"
            "• Send a **photo** directly → Get ImgBB/Envs.sh link.\n"
            "• Send a **text** in the following format → Get Graph.org post.\n\n"
            "📝 **Custom Title**:\n"
            "```txt\n"
            "Title: {title}\n{content}\n"
            "```\n\n"
            "✅ **Example**:\n"
            "```txt\n"
            "Title: My First Graph.org Post\n"
            "This is the content of my first post!\n\n"
            "Here's a list of what I like:\n"
            "- Programming 💻\n"
            "- Reading 📚\n"
            "- Traveling ✈️\n"
            "- Music 🎵\n"
            "```\n\n"
            "🔗 **About Graph.org**:\n"
            "Graph.org is a minimalist publishing tool (alternative to Telegra.ph, which is banned in India) that allows you to share beautifully formatted posts with text, images, and more.\n\n"
            "🖼️ **About ImgBB & Envs.sh**:\n"
            "- **ImgBB** → Permanent image hosting with fast sharing links.\n"
            "- **Envs.sh** → Temporary hosting (⚠️ files may be deleted after 30 days).\n\n"
            "🌟 **Get Started Now!** Just send a photo or formatted text message and let me handle the rest 🚀"
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👨‍💻 My Creator", url="https://t.me/The_proGrammerr"
                    ),
                    InlineKeyboardButton(
                        "🛠 Source Code",
                        url="https://github.com/Ns-AnoNymouS/Telegraph-Uploader",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📌 Updates", url="https://t.me/NsBotsOfficial"
                    ),
                    InlineKeyboardButton("❤️ Support", url="https://t.me/amcDevSupport"),
                ],
            ]
        ),
        quote=True,
    )


def upload_file(file_path):
    """
    Uploads file to ImgBB (if API key is set).
    Falls back to envs.sh if ImgBB fails or API key missing.
    """
    imgbb_key = getattr(Config, "IMGBB_API_KEY", None)
    logger.debug("Attempting to upload file: %s", file_path)

    # 1. Try ImgBB first (if key exists)
    if imgbb_key:
        logger.debug("ImgBB API key found. Uploading to ImgBB...")
        try:
            with open(file_path, "rb") as f:
                files = {"image": f}
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    params={"key": imgbb_key},
                    files=files,
                    timeout=15,
                )

            if response.ok:
                data = response.json()["data"]
                return {
                    "provider": "imgbb",
                    "url": data["url"],
                    "delete_url": data.get("delete_url"),
                }
            else:
                logger.warning("ImgBB upload failed: %s", response.text)

        except Exception as e:
            logger.error("Error uploading to ImgBB: %s", e, exc_info=True)

    # 2. Fallback: use envs.sh
    logger.debug("Falling back to envs.sh upload...")
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post("https://envs.sh", files=files, timeout=15)

        if response.ok:
            url = response.text.strip()
            logger.info("File uploaded to envs.sh: %s", url)
            return {"provider": "envs.sh", "url": url}
        else:
            logger.error("envs.sh upload failed: %s", response.text)

    except Exception as e:
        logger.critical("All upload methods failed: %s", e, exc_info=True)


@bot.on_message(filters.photo & filters.incoming & filters.private)
async def photo_handler(_: Bot, message: Message) -> None:
    """Handles incoming photo messages by uploading them to cloud providers."""

    try:
        logger.debug("Received photo from user_id=%s", message.from_user.id)
        msg = await message.reply_text("Processing....⏳", quote=True)

        location = f"./{message.from_user.id}{time.time()}/"
        start_time = time.time()
        logger.debug("Downloading photo to %s", location)

        file = await message.download(
            location, progress=progress, progress_args=(msg, start_time)
        )
        logger.info("Photo downloaded: %s", file)

        await msg.edit(
            "📥 **Download Complete!**\n\n"
            "☁️ Now uploading your file to the **cloud provider**..."
        )

        media_data = upload_file(file)
        if not media_data:
            logger.warning("Upload failed for file: %s", file)
            await msg.edit(
                "⚠️ Oops! We couldn’t upload your media file.\nPlease try again in a while."
            )
            return

        else:
            buttons = [[InlineKeyboardButton("🌐 View Image", url=media_data["url"])]]

            text = (
                f"[\u200B]({media_data['url']})✅ **Upload Successful!**\n\n"
                f"🖼️ [Click here to view the image]({media_data['url']})\n\n"
                f"📡 **Provider:** `{media_data['provider']}`\n\n"
                f"🔗 **Direct Link:** `{media_data['url']}`\n\n"
            )

            if media_data["provider"].lower() == "envs.sh":
                text += (
                    "\n⚠️ **Note:**\n\nFiles uploaded to **Envs.sh** may be automatically deleted "
                    "after **30 days**. This is **not** a permanent storage option.\n\n"
                )

            if media_data.get("delete_url"):
                buttons.append(
                    [
                        InlineKeyboardButton(
                            "🗑️ Delete Image", url=media_data["delete_url"]
                        )
                    ]
                )

            await msg.edit(
                text,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=False,
            )

    except FileNotFoundError:
        pass
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        await msg.edit(f"**Error:**\n{e}")
    finally:
        if os.path.exists(file):
            os.remove(file)
            os.rmdir(location)


@bot.on_message(filters.text & filters.incoming & filters.private)
async def text_handler(_: Bot, message: Message) -> None:
    """Handles text messages by creating Graph.org posts."""

    try:
        logger.debug("Received text message from user_id=%s", message.from_user.id)
        msg = await message.reply_text("Processing....⏳", quote=True)

        short_name = "Ns Bots"
        logger.debug("Creating Telegraph account with short_name=%s", short_name)

        user = Telegraph(domain=Config.DOMAIN).create_account(short_name=short_name)
        access_token = user.get("access_token")

        logger.debug("Access token acquired for Telegraph API")
        content = message.text.html
        content = re.sub(EMOJI_PATTERN, "", content).replace("</emoji>", "")

        title = re.findall(TITLE_PATTERN, content)
        if len(title) != 0:
            title = title[0]
            logger.debug("Custom title extracted: %s", title)
            content = "\n".join(content.splitlines()[1:])
        else:
            title = message.from_user.first_name
            logger.debug("No custom title found. Using user name: %s", title)

        content = content.replace("\n", "<br>")
        author_url = (
            f"https://telegram.dog/{message.from_user.username}"
            if message.from_user.id
            else None
        )

        response = Telegraph(
            domain=Config.DOMAIN, access_token=access_token
        ).create_page(
            title=title,
            html_content=content,
            author_name=str(message.from_user.first_name),
            author_url=author_url,
        )
        path = response["path"]
        await msg.edit(f"https://{Config.DOMAIN}/{path}")
    except ValueError as e:
        logger.error(e)
        await msg.edit("Unable to generate instant view link.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        await msg.edit(f"**Error:**\n{e}")


if __name__ == "__main__":
    bot.run()
