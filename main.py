from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# BOT_TOKEN
from config import BOT_TOKEN, MAIN_ADMIN

# Database
from db import Database

db = Database("Tiki_database.db")

# massage_handler
from message_handler import message_handler

# check user
from check import check_user

# main_admin
from main_admin import admin
# to remove channels
from remove_channel import remove_channel, inline_message
# list of channels
from get_channels import get_channels


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if str(user.id) in MAIN_ADMIN:
        commands = [BotCommand(command="start", description="Botni ishga tushurish"),
                    BotCommand(command="admin", description="Admin panelga o'tish"),
                    BotCommand(command="get_channels", description="Bazadagi kanallarni ko'rish"),
                    BotCommand(command="remove", description="Bazadan kannallarni o'chirish")]
        await context.bot.set_my_commands(commands)
    else:
        command = [BotCommand(command="start", description="Botni ishga tushurish")]
        await context.bot.set_my_commands(command)

    if check_user(user):
        await update.message.reply_html(
            f"Salom <b>{check_user(user).get('full_name')}</b> \n"
            f"Sizni yana botimizda ko'rganimizdan xursandmiz 😊"
        )
    else:
        await update.message.reply_html(
            f"Salom <b> Yangi foydalanuvchi </b> \n"
            f"Botimizga Hush kelibsiz! 😊"
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler('admin', admin))
    app.add_handler(CommandHandler('remove', remove_channel))
    app.add_handler(CommandHandler('get_channels', get_channels))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(CallbackQueryHandler(inline_message))

    app.run_polling()


if __name__ == '__main__':
    main()
