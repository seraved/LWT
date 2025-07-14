
from telegram.ext import ContextTypes
from telegram import Update, Message
from bot.states import States
from bot.keyboards import main_menu, media_list_keyboard
from services.media import MediaService
from entities.media import MediaDTO, MediaType
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.getters import get_user_id, get_message_text


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return States.MAIN_MENU

    await query.answer()

    if query.data == "add_media":
        await query.edit_message_text("Введите название:")
        return States.ADD_MEDIA  # Переход в состояние добавления

    if query.data == "list_media":
        return await show_media_list(update, context, page=1)


async def add_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик добавления контента"""
    if update.message is None:
        return States.MAIN_MENU

    if (user_id := get_user_id(update.message)) is None:
        return States.MAIN_MENU
    if (title := get_message_text(update.message)) is None:
        return States.MAIN_MENU

    # TODO FIX IT MOC
    user_id = 1
    await MediaService().add_media(
        media_data=MediaDTO(
            title=title,
            media_type=MediaType.MOVIE,
            user_id=user_id,
        )
    )
    await update.message.reply_text(
        "✅ Запись добавлена!",
        reply_markup=main_menu(),
    )
    return States.MAIN_MENU


async def show_media_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    user_id = update.effective_user.id
    # TODO FIX THIS MOC
    user_id = 1
    service = MediaService()
    media_items = await service.get_user_media(user_id, page)
    total_items = await service.get_media_count(user_id)
    total_pages = (total_items + 2) // 3  # Округляем вверх

    if not media_items:
        await update.callback_query.edit_message_text(
            "Ваш список пуст",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("➕ Добавить", callback_data="add_media")]])
        )
        return States.MAIN_MENU

    items_text = "\n".join(
        f"{i+1}. {item.title} {'✅' if item.watched else ''}"
        for i, item in enumerate(media_items)
    )

    await update.callback_query.edit_message_text(
        f"📋 Ваши записи (стр. {page}/{total_pages}):\n\n{items_text}",
        reply_markup=media_list_keyboard(page, total_pages))
    return States.VIEWING_LIST


async def page_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = int(update.callback_query.data.split("_")[1])
    return await show_media_list(update, context, page)
