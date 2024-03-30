import logging
import logging
import os
import socket

import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TEAM_NAME, HASH_CODE = range(2)


# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["OK"]]

    await update.message.reply_text(
        f"Привет, участник {os.getenv('EVENT_NAME')} \nПожалуйста, заполни необходимую информацию о своей команде",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )


async def check_tag_exist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)

    check_tag = requests.get(
        f"http://{host_ip}:5000/api/{update.message.from_user.username}&{update.effective_chat.id}").text

    if check_tag == "Yes":
        message = "You are already participating in the draw!\nAll further information is waiting for you in the group"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    elif check_tag == "No":
        message = "Sorry, you are not registered yet \nFill out the form and you will be on the list of participants!"
        requests.post(f"http://{host_ip}:5000/api/{update.message.from_user.username}&{update.effective_chat.id}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    else:
        message = "Sorry, something went wrong \nPlease text to @carpfield"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def cancel_info_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


async def start_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("")
    return TEAM_NAME


async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    allow_permissions = ["carpfield"]

    keyboard = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message.from_user.username in allow_permissions:
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="Please, enter a tag")
        await update.message.reply_text("Please, enter a tag", reply_markup=reply_markup)

        # return ID
    else:
        return ConversationHandler.END


async def reply_markup_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "cancel":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Action canceled")
        return ConversationHandler.END


async def team_name_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return HASH_CODE


async def hash_code_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return


if __name__ == "__main__":
    bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    # Telegram handlers
    start_handler = CommandHandler("start", start)

    information_start = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("OK"), start_information)],
        states={
            TEAM_NAME: [MessageHandler(filters.TEXT, team_name_info)],
            HASH_CODE: [MessageHandler(filters.Regex(""), hash_code_info)]
        },
        fallbacks=[CallbackQueryHandler(reply_markup_cancel), CommandHandler("/cancel", cancel_info_conv)]
    )

    
    # winner_handler = ConversationHandler(
    #     entry_points=[CommandHandler("send_winner_message", check_permissions)],
    #     states={
    #         ID: [MessageHandler(filters.Regex("^@"), read_tag)],
    #     },
    #     fallbacks=[CallbackQueryHandler(reply_markup_cancel)]
    # )

    # Telegram add field
    bot.add_handler(start_handler)
    bot.add_handler(information_start)

    bot.run_polling(allowed_updates=Update.ALL_TYPES)
