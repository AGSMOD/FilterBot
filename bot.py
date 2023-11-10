# bot.py
import os
from pymongo import MongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Retrieve environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN','')
MONGO_URI = os.environ.get('MONGO_URI','')
MONGO_NAME = os.environ.get('MONGO_NAME', 'your_default_mongo_name')
API_ID = int(os.environ.get('API_ID',''))
API_HASH = os.environ.get('API_HASH','')
FORCE_SUBSCRIBE = os.environ.get('FORCE_SUBSCRIBE','', False)  # Default to False if not set
LOG_CHANNEL = os.environ.get('LOG_CHANNEL', 'your_default_log_channel')
BOT_PIC = os.environ.get('BOT_PIC', 'path/to/your/bot_pic.jpg')

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database()
users_collection = db.users

def is_subscribed(user_id):
    user_data = users_collection.find_one({'user_id': user_id})
    return user_data and user_data.get('subscribed', False)

def add_user(user_id):
    user_data = {'user_id': user_id, 'subscribed': False}
    users_collection.insert_one(user_data)

def subscribe_user(user_id):
    users_collection.update_one({'user_id': user_id}, {'$set': {'subscribed': True}})

def start(update, context):
    user_id = update.effective_user.id
    if FORCE_SUBSCRIBE and not is_subscribed(user_id):
        update.message.reply_text('Welcome! Please subscribe to continue.')
        # You can implement subscription logic here
    else:
        # Set a custom profile picture for the bot
        context.bot.setProfilePhoto(photo=open(BOT_PIC, 'rb'))

        keyboard = [
            [InlineKeyboardButton("Go to Website", url="http://example.com")],
            [InlineKeyboardButton("Subscribe Now", callback_data='subscribe')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Hello! I am your bot.', reply_markup=reply_markup)

def welcome_message(update, context):
    user_id = update.effective_user.id
    if FORCE_SUBSCRIBE and not is_subscribed(user_id):
        return  # Ignore messages from non-subscribed users
    keyboard = [
        [InlineKeyboardButton("Go to Website", url="http://example.com")],
        [InlineKeyboardButton("Another Command", callback_data='another_command')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Thanks for subscribing.', reply_markup=reply_markup)

def inline_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'subscribe':
        subscribe_user(user_id)
        query.edit_message_text(text="You are now subscribed!")

    elif query.data == 'another_command':
        query.edit_message_text(text="You pressed 'Another Command'")
        # Add more conditions based on your button actions

def log_message(context, message):
    # Log the message to a designated channel
    context.bot.send_message(LOG_CHANNEL, message)

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.TEXT & ~Filters.COMMAND, welcome_message))
    dp.add_handler(CallbackQueryHandler(inline_button_handler))  # Added callback handler

    # Example: Log a welcome message to the designated channel
    log_message(updater, "Bot is online and ready!")

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
