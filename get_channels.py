from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from config import MAIN_ADMIN
from remove_channel import channels


async def get_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if str(user.id) in MAIN_ADMIN:
        if len(channels) == 0:
            await update.message.reply_html("<b> Ma'lumotlar ba'zasi bo'sh! </b>")
        else:
            channel_buttons = []
            try:
                for channel in channels:
                    channel = dict(channel)
                    channel_buttons.append(
                        [InlineKeyboardButton(
                            text=f"🔷🔹 {channel.get('name')}  🔹🔷",
                            url=f"https://t.me/{channel.get('link')[1:]}"
                        )])
            except BadRequest as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"Error: {str(e)}")

            await update.message.reply_html(
                text="<b> Ma'lumotlar bazasidagi kanallar ro'yxati: </b>",
                reply_markup=InlineKeyboardMarkup(channel_buttons)
            )
    else:
        await update.message.reply_html(
            text="<b> Siz adminlar ro'yxatida yo'qsiz! </b>"
        )
