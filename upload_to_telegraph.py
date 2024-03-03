import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import os
import time
from config import Config
from helpers import progress
from telegraph import upload_file, Telegraph
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
        "⍟ I can create an instant view link for your text.\n"
        "⍟ I can create a post in telegra.ph if you send any text.\n"
        "(You can send text in the format `post content|TITLE`)\n\n"
        "Create your own [𝗙𝗼𝗿𝗸 𝗡𝗼𝘄](https://github.com/Ns-AnoNymouS/Telegraph-Uploader)",
        disable_web_page_preview=True,
        quote=True,
        parse_mode="markdown"  # Change "HTML" to "markdown"
    )



@telegraphbot.on_message(filters.photo & filters.incoming)
async def telegraph(c, m):
    """Uploading to photo to telegra.ph 
       and sending photo link to user"""

    try:
        send_message = await m.reply_text(
            "Processing....⏳", 
            quote=True
        )
        location = f'./{m.from_user.id}{time.time()}/'
        start_time = time.time()
        file = await m.download(
            location,
            progress=progress,
            progress_args=(send_message, start_time)
        )
        try:
            media_upload = upload_file(file)
        except Exception as e:
            print('An Error occurred', e)
            await send_message.edit(f'**Error:**\n{e}')
        telegraph_link = f'https://telegra.ph{media_upload[0]}'
        await send_message.edit(
            telegraph_link
        )
    except:
        pass


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

    except:
        pass


telegraphbot.run()
