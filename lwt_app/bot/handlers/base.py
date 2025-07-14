
from telegram.ext import ContextTypes
from telegram import Update
from bot.states import States
from bot.keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return States.MAIN_MENU

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=main_menu()
    )
    return States.MAIN_MENU


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is None:
        return States.MAIN_MENU

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Главное меню:",
        reply_markup=main_menu()
    )
    return States.MAIN_MENU
