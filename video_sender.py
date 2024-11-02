from telegram import Update
from validators import url
from downloader import all_downloader


async def video_sender(update: Update, text):

    if url(text):
        try:
            data = all_downloader(text)

            if data:
                 await update.message.reply_video(
                    video=data,
                    caption="<b> 💎 @TikiDownloaderBot 💎 </b>",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_html(
                    text="<b> Video yuklashda xatolik yuz berdi! 😔 </b>"
                )
        except:
            await update.message.reply_html(
                text="<b>  Video yuklashda xatolik yuz berdi! 😔 </b>"
            )
    else:
        await update.message.reply_html(
            text="<b> Siz noto'g'ri link yubordingiz! 😕 </b>"
        )
