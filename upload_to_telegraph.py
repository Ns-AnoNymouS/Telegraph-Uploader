import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import time
from config import Config
from telegraph import Telegraph
from pyrogram import Client, filters

telegraphbot = Client("TELEGRAPH",
                      bot_token=Config.BOT_TOKEN,
                      api_id=Config.API_ID,
                      api_hash=Config.API_HASH,
                      parse_mode="markdown",
                      workers=100)

@telegraphbot.on_message(filters.command('start') & filters.incoming)
async def start_handlers(c, m):
    await m.reply_text(
        "Hello **Dear!**\n\n"
        "I am a telegra.ph uploader.\n\n"
        "⍟ I can create a instant view link for your text.\n"
        "⍟ I can create post in telegra.ph if you send any text.\n"
        "(You can send text in format `post content|TITLE`)\n\n"
        "Create your own [𝗙𝗼𝗿𝗸 𝗡𝗼𝘄](https://github.com/Ns-AnoNymouS/Telegraph-Uploader)",
        disable_web_page_preview=True,
        quote=True
    )

@telegraphbot.on_message(filters.text & filters.incoming)
async def text_handler(c, m):
    """Creating instant view link
       by creating post in telegra.ph 
       and sending photo link to user"""

    try:
        short_name = "Ns Bots"
        new_user = Telegraph().create_account(short_name=short_name)
        auth_url = new_user["auth_url"]
        title = m.from_user.first_name
        content = m.text
        if '|' in m.text:
            content, title = m.text.split('|')
        content = content.replace("\n", "<br>")
        author_url = f'https://telegram.dog/{m.from_user.username}' if m.from_user.id else None

        try:
            response = Telegraph().create_page(
                title=title,
                html_content=content,
                author_name=str(m.from_user.first_name),
                author_url=author_url
            )
        except Exception as e:
            print(e)
        await m.reply_text("https://telegra.ph/{}".format(response["path"]))

    except Exception as e:
        logger.error(f"Error in text_handler: {e}")

telegraphbot.run()
graphbot.run()
