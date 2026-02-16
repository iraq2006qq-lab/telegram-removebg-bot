import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جارِ تفريغ الخلفية...")

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_bytes},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
    )

    if response.status_code == 200:
        await update.message.reply_document(response.content, filename="no-bg.png")
    else:
        await update.message.reply_text("❌ صار خطأ بتفريغ الصورة، جرّب مرة ثانية.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()
