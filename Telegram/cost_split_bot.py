from ast import Call
import os
from dotenv import load_dotenv
from telegram import *
from telegram import replymarkup
from telegram.ext import *
import logging
from requests import *

load_dotenv("./.env")
TOKEN = os.getenv("token")

print("Bot started!")

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
level=logging.INFO
)

logger = logging.getLogger(__name__)

splitEven = "Split Evenly"
splitSpecifically = "Split Specifically"

keyboard = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
         ['0']
]

yes_button = "Yes"
no_button = "No"

def afterImage(update: Update, context: CallbackContext):
    split_buttons = [[KeyboardButton(splitEven)], [KeyboardButton(splitSpecifically)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am cost split bot! Please send in a picture of your receipt!", reply_markup=ReplyKeyboardMarkup(keyboard=split_buttons, one_time_keyboard=True))

def get_num(update, context: CallbackContext):
    decision = update.message.text
    if decision == "Split Evenly":
        num_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text="How many people do you want to split this with?", reply_markup=num_keyboard)
    elif decision == "Split Specifically":
        return

def check_numeric(update, context: CallbackContext):
    reply = update.message.text
    if reply.isnumeric():
        return True
    return False

def not_numeric(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You sent an incorrect input. Please send a numeric input.")

def split_even_by_num(update: Update, context: CallbackContext):
    split_num = update.message.text
    # input total here
    ###final_split = total / split_num
    confirm_buttons = [[KeyboardButton(yes_button)], [KeyboardButton(no_button)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your total amount of total will be split among {split_num} person(s). Is this correct?", reply_markup=ReplyKeyboardMarkup(keyboard=confirm_buttons, one_time_keyboard=True))
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
    dispatcher.add_handler(CommandHandler("start", afterImage))

    # Add Split Evenly handler
    dispatcher.add_handler(MessageHandler(Filters.text, get_num))



    # STUCK HERE NEED TO USE get_num TO NEXT MESSAGE STEP #
    # Check if message is numeric
    while check_numeric==False:
        not_numeric
        check_numeric
    dispatcher.add_handler(MessageHandler(Filters.text, split_even_by_num))

    # Add error handling
    dispatcher.add_error_handler(error_handling)

    updater.start_polling()

    updater.idle()

if __name__=="__main__":
    main()

# Input image

# Returns dictionary of information

# return receipt_info{
# "receiptID" : 22, 
# "item_dict": {apple: 1, banana: 1, carrot:1}, 
# "quantity_list": [1, 1, 1],
# "price_list": [1, 2, 3],
# "total_cost": 6
# }

# Split dictionary into variables
# def split_info(receipt_info):
#     receiptID = receipt_info[0]
#     item_dict = receipt_info[1]
#     quantity_list = receipt_info[2]
#     price_list = receipt_info[3]
#     total_cost = receipt_info[4]

#     return receiptID, item_dict, quantity_list, price_list, total_cost

# # Get number of people to split 
# def split_equally(message):
#     num_to_split = message


# # Create dictionary of items and numbers
# def item_dictionary(item_list, quantity_list)