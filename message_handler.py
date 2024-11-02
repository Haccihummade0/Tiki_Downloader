from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes

# Database
from db import Database

db = Database("Tiki_database.db")

# majburiy obuna
from mandatory_subscription import mandatory_subscription


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    state = context.user_data.get('state')

    if state == "ADMIN_HOME":
        if text == "🟢 Add channel":

            context.user_data['state'] = "ADD_CHANNEL"

            await update.message.reply_html(
                text="Kanal qo'shish uchun namuna: \n\n"
                     "channel name++username \n\n"
                     "Abcd++@Abcd"
            )

        elif text == "🟡 Send ads":

            context.user_data['state'] = "ADMIN_ADS"
            await update.message.reply_html(
                text="Reklama matnini kiriting!"
            )


        elif text == "❌ Chiqish":

            del context.user_data['state']

            await update.message.reply_html(
                text="Siz admin panelidan chiqdingiz!",
                reply_markup=ReplyKeyboardRemove()
            )

    elif state == "ADD_CHANNEL":
        data = text.split("++")

        try:
            if len(data) == 2:
                status = await context.bot.get_chat_member(
                    chat_id=data[-1],
                    user_id=context.bot.id,
                )

                if status.status.title() == "Administrator":
                    db.create_channel(
                        name=data[0],
                        link=data[1]
                    )
                    # Channel state
                    context.user_data['state'] = "ADMIN_HOME"
                    await update.message.reply_html(
                        text=f"✅ {data[0]} kanali qo'shildi!",
                        reply_markup=ReplyKeyboardMarkup([
                            [KeyboardButton("🟢 Add channel")],
                            [KeyboardButton("🟡 Reklama yuborish")],
                            [KeyboardButton("❌ Chiqish")]], resize_keyboard=True)
                    )
                else:
                    await update.message.reply_html(
                        text="❌ Namuna bo'yicha kiriting:"
                    )
            else:
                await update.message.reply_html(
                    text="❌ Namuna bo'yicha kiriting:"
                )
        except:
            await update.message.reply_html(
                text="❌ Botni kanalga admin qiling!"
            )

    elif state == "ADMIN_ADS":
        users = db.get_users()

        k = 0
        for user in users:
            try:
                await context.bot.send_message(
                    chat_id=user.get("chat_id"),
                    text=text,
                    parse_mode="HTML"
                )
                k += 1
            except:
                print("Error")

        # Change state
        context.user_data['state'] = 'ADMIN_HOME'

        await update.message.reply_html(
            text=f"✅ Reklama {k} ta foydalanuvchiga yuborildi."
        )

    else:
        await mandatory_subscription(update, text)
