
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from telegram import Update
from bot.states import States

from bot.keyboards import base as base_markup


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
            "LWT Бот Готов! \n"
        ),
        reply_markup=base_markup.main_menu(),
    )
    return States.MAIN_MENU


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.callback_query is None:
        return States.START_MENU
    # await update.callback_query.answer()
    # await update.callback_query.edit_message_text(
    #     "Главное меню:",
    #     reply_markup=base_markup.main_menu()
    # )
    return await main_menu(update, context)


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Отменено.")
    return ConversationHandler.END
