import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import pytesseract
import requests
from io import BytesIO

TOKEN = os.getenv("7794792250:AAHv_6fXARNtByXCwOxAsRxNuFAUNeZs5sk")  # Set token via environment variable

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me an image with text, and I'll try to read it!")

def image_handler(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1]  # Get the highest resolution image
    photo_file = photo.get_file()
    response = requests.get(photo_file.file_path)
    img = Image.open(BytesIO(response.content))

    # OCR to extract text
    text = pytesseract.image_to_string(img)
    update.message.reply_text(text if text else "Sorry, I couldn't read any text.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
