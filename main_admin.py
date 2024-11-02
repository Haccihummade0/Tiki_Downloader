from telegram import (Update, KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import ContextTypes

from config import MAIN_ADMIN


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if str(user.id) in MAIN_ADMIN:

        context.user_data['state'] = "ADMIN_HOME"

        await update.message.reply_html(
            text="<b> Admin panelga xush kelibsiz </b>",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("🟢 Add channel")],
                [KeyboardButton("🟡 Send ads")],
                [KeyboardButton("❌ Exit")]], resize_keyboard=True, one_time_keyboard=True)
        )
    else:
        await update.message.reply_html(
            text="<b> Siz adminlar ro'yxatida yo'qsiz! </b>"
        )
