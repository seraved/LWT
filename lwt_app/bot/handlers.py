from telegram.ext import ContextTypes
from telegram import Update, Message
from bot.states import States
from bot.keyboards import main_menu
from services.media import MediaService
from entities.media import MediaDTO, MediaType


def get_user_id(message: Message) -> int | None:
    if message.from_user is None:
        return None
    return message.from_user.id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=main_menu()
    )
    return States.MAIN_MENU


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return States.MAIN_MENU

    await query.answer()

    if query.data == "add_media":
        await query.edit_message_text("Введите название:")
        return States.ADD_MEDIA  # Переход в состояние добавления


async def handle_add_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None:
        return States.MAIN_MENU

    if (user_id := get_user_id(update.message)) is None:
        return States.MAIN_MENU

    if (title := update.message.text) is None:
        # TODO пустой текст
        return States.MAIN_MENU
    # TODO FIX IT MOC
    user_id = 1
    await MediaService().add_media(
        media_data=MediaDTO(
            title=title,
            media_type=MediaType.MOVIE,
            user_id=user_id,  # TODO MOC
        )
    )
    await update.message.reply_text("✅ Запись добавлена!")
    return States.MAIN_MENU
