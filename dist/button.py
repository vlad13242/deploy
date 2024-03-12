from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater
from telegram import Update

def button_click(update: Update, context):
    query = update.callback_query
    user_username = query.from_user.username
    button_data_clicked = query.data
    bot = Bot(token='6791691843:AAFPIy_GLYC7-eRDSb1okBF1bPZ2IUsD_oU')
    
    user_info = f"Пользователь ник: {user_username}\n"
    
    admin_chat_id = "214864280"
    print(f"{user_info} Нажато на кнопку {button_data_clicked}.")
    bot.send_message(admin_chat_id, f"{user_info} Нажато на кнопку {button_data_clicked}")
    

    query.answer(f"An administrator will contact you soon")

updater = Updater(token='6791691843:AAFPIy_GLYC7-eRDSb1okBF1bPZ2IUsD_oU', use_context=True)
dp = updater.dispatcher

dp.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
updater.idle()
