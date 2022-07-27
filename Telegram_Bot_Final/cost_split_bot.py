# Imports
import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *
import logging
from requests import *
import veryfi_func

# Obtain Bot Token
load_dotenv()
TOKEN = os.getenv("token")

print("Bot started!")

# Initiate Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Create States
PHOTO, SPLIT_CHOICE, NUM_PEOPLE, END = range(4)

# Create Variables
receipt_total = 0

split_keyboard = [[KeyboardButton("Split Evenly")], [KeyboardButton("Split Specifically")]]

num_keyboard = [[KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9")],
                [KeyboardButton("4"),KeyboardButton("5"),KeyboardButton("6")],
                [KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3")],
                                        [KeyboardButton("0")]]

# /start - Start bot command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello, I am cost split bot! Please send in a picture of your receipt!"
    )
    return PHOTO

# Image Recognition
def photo(update, context:CallbackContext):
    file_dict = context.bot.get_file(update.message.photo[-1].file_id)
    downloaded_file = file_dict.download()
    output = veryfi_func.read_img(downloaded_file)
    global receipt_total
    receipt_total = output
    print(receipt_total)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Which way do you want to split this?", 
        reply_markup=ReplyKeyboardMarkup(keyboard=split_keyboard, one_time_keyboard=True)
    )
    return SPLIT_CHOICE

# Obtain number of people to split with
def get_num(update:Update, context: CallbackContext):
    decision = update.message.text
    if decision == "Split Evenly":
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="How many people do you want to split this with?", 
            reply_markup=ReplyKeyboardMarkup(keyboard=num_keyboard, one_time_keyboard=True)
        )
        return NUM_PEOPLE
        # try invoking function here
    elif decision == "Split Specifically":
        return

# Confirmation of information
def split_even_by_num(update, context:CallbackContext):
    split_num = int(update.message.text)
    print(split_num)
    final_split = round(receipt_total / split_num, 2)
    confirm_buttons = [[KeyboardButton("Yes")], [KeyboardButton("No")]]
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Your total amount of {receipt_total} will be split among {split_num} person(s). The final split will be {final_split} per person. Is this correct?", 
        reply_markup=ReplyKeyboardMarkup(keyboard=confirm_buttons, one_time_keyboard=True)
    )
    return END

# Ending Statement
def end(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Thank you for using our bot, goodbye!"
    )
    return ConversationHandler.END

# /cancel - Exit bot command
def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s cancelled the conversation.", user.first_name)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"See you soon!"
    )
    return ConversationHandler.END

# Error handling
def error_handling(update: Update, context: CallbackContext) -> None:
    """Logs all errors or message caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)

# main
def main():
    # Create updater
    updater = Updater(TOKEN)

    # Initiate dispatcher to register the different handlers
    dispatcher = updater.dispatcher

    # Initiate Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
            SPLIT_CHOICE: [MessageHandler(Filters.text, get_num)],
            NUM_PEOPLE: [MessageHandler(Filters.text, split_even_by_num)],
            END: [MessageHandler(Filters.text, end)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error_handling)

    # Pollng
    updater.start_polling()

    updater.idle()

if __name__=="__main__":
    main()