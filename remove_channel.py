from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import ContextTypes

# Database
from db import Database

db = Database("Tiki_database.db")
from config import MAIN_ADMIN

channels = db.get_channels()

keyboard = [[InlineKeyboardButton(f"{channel.get('name')}", callback_data=f"{channel.get('link')}")]
            for channel in channels]

reply_markup = InlineKeyboardMarkup(keyboard)


async def remove_channel(update, context):
    user = update.effective_user

    if str(user.id) in MAIN_ADMIN:
        if len(channels) == 0:
            await update.message.reply_html("<b> There is no channels to delete </b>")
        else:
            await update.message.reply_html("<b> Choose a channel to remove: </b>", reply_markup=reply_markup)

    else:
        await update.message.reply_html(
            text="<b> Siz adminlar ro'yxatida yo'qsiz! </b>"
        )


# Callback function to handle button press
async def inline_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    callback_data = query.data

    for channel in channels:
        if not callback_data:
            await update.message.reply_html("<b> There is no channel to delete! </b>")

        if callback_data == channel.get('link'):
            link = channel.get('link')
            name = channel.get('name')

            # Remove the channel from the database
            db.delete_channel(name, link)

            await query.edit_message_text(f"<b> {channel.get('name')} </b> channel removed successfully!")
        else:
            await update.message.reply_html("<b> There is no channel to delete! </b>")
