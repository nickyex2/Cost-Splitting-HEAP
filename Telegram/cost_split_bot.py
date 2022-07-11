from ast import Call
import os
from turtle import Turtle
from dotenv import load_dotenv
from telegram import *
from telegram import replymarkup
from telegram.ext import *
import logging
from requests import *
import tesseract_func
import veryfi_func

load_dotenv("./.env")
TOKEN = os.getenv("token")

print("Bot started!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

receipt_total = 0

split_buttons = [[KeyboardButton("Split Evenly")], [KeyboardButton("Split Specifically")]]

num_keyboard = [[KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9")],
                [KeyboardButton("4"),KeyboardButton("5"),KeyboardButton("6")],
                [KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3")],
                                        [KeyboardButton("0")]]

# /start command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am cost split bot! Please send in a picture of your receipt!")

def photo(update, context:CallbackContext):
    file_dict = context.bot.get_file(update.message.photo[-1].file_id)
    print(file_dict)
    downloaded_file = file_dict.download()
    output = veryfi_func.read_img(downloaded_file)
    receipt_total = output
    print(receipt_total)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok TQ.", reply_markup=ReplyKeyboardMarkup(keyboard=split_buttons, one_time_keyboard=True))

def get_num(update:Update, context: CallbackContext):
    decision = update.message.text
    if decision == "Split Evenly":
        # num_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="How many people do you want to split this with?", reply_markup=ReplyKeyboardMarkup(keyboard=num_keyboard, one_time_keyboard=True))
        # num = update.message.text
        print("yo")
    elif decision == "Split Specifically":
        return

def split_even_by_num(update, context:CallbackContext):
    print('back')
    split_num = int(update.message.text)
    print(split_num)
    final_split = round(receipt_total / split_num, 2)
    confirm_buttons = [[KeyboardButton("Yes")], [KeyboardButton("No")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your total amount of {receipt_total} will be split among {split_num} person(s). The final split will be {final_split} per person. Is this correct?", reply_markup=ReplyKeyboardMarkup(keyboard=confirm_buttons, one_time_keyboard=True))
    ###return final_split

# Define receive telegram handles to message them

# Define /back command
# Define /reset command
# Define /end command

def error_handling(update: Update, context: CallbackContext) -> None:
    """Logs all errors or message caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)

def main():
    # Create updater
    updater = Updater(TOKEN)

    # Initiate dispatcher to register the different handlers
    dispatcher = updater.dispatcher

    # Add /start handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Process photo
    dispatcher.add_handler(MessageHandler(Filters.photo, photo))

    # Add Split Evenly handler
    dispatcher.add_handler(MessageHandler(Filters.text, get_num))

    # STUCK HERE NEED TO USE get_num TO NEXT MESSAGE STEP #
    # Check if message is numeric
    # dispatcher.add_handler(MessageHandler(Filters.text, check_numeric))

    # while check_numeric==False:
    #     dispatcher.add_handler(MessageHandler(Filters.text, not_numeric))
    #     dispatcher.add_handler(MessageHandler(Filters.text, check_numeric))

    dispatcher.add_handler(MessageHandler(Filters.text, split_even_by_num))

    # Add error handling
    dispatcher.add_error_handler(error_handling)

    updater.start_polling()

    updater.idle()

if __name__=="__main__":
    main()