import os
import requests
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

def handle_photo(update: Update, context: CallbackContext):
    update.message.reply_text("⏳ جارِ تفريغ الخلفية...")

    photo_file = update.message.photo[-1].get_file()
    image_bytes = photo_file.download_as_bytearray()

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_bytes},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
    )

    if response.status_code == 200:
        update.message.reply_document(response.content, filename="no-bg.png")
    else:
        update.message.reply_text("❌ صار خطأ بتفريغ الصورة، جرّب مرة ثانية.")

updater = Updater(TELEGRAM_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
updater.start_polling()
updater.idle()
