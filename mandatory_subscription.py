from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ContextTypes


from check import check_user
from db import Database

db = Database("Tiki_database.db")
from video_sender import video_sender


async def mandatory_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user



    check_user(user)

    channel_status = []
    channel_buttons = []
    channels = db.get_channels()

    for i in channels:

        try:
            i = dict(i)
            channel_buttons.append(
                [InlineKeyboardButton(
                    text=f"🔷🔹 {i.get('name')}  🔹🔷",
                    url=f"https://t.me/{i.get('link')[1:]}"
                )]
            )

            chat_member = await update.message._bot.get_chat_member(i.get('link'), user.id)

            status = chat_member.status.title()
            channel_status.append(status)

        except BadRequest as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    if "Left" in channel_status:
        await update.message.reply_html(
            text="<b> Botimizdan foydalanish uchun kanallarga obuna bo'ling! </b>",
            reply_markup=InlineKeyboardMarkup(channel_buttons)
        )
    else:
        await video_sender(update, text=text)
