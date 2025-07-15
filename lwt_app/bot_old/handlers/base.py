
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from telegram import Update
from bot_old.states import States

from bot_old.keyboards import base as base_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return States.START_MENU

    await update.message.reply_text(
        text=(
            "LWT Бот Приветствует Тебя! \n"
            "Для начала работы нужно авторизоваться. \n"
        ),
        reply_markup=base_markup.unauth_keyboard(),
    )
    return States.START_MENU


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None:
        return States.START_MENU

    await update.message.reply_text(
        text=(
            "Хотите Добавить или Просмотреть что уже добавлено? \n"
        ),
        reply_markup=base_markup.main_menu(),
    )
    return States.MAIN_MENU

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Отменено.")
    return ConversationHandler.END
