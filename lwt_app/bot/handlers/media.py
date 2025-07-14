
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardRemove, Update

from bot.states import States
from bot.keyboards import media, base
from bot.keyboards import constants as kb_val
from services.media import MediaService
from entities.media import NewMediaDTO
from utils import getters as getter
from utils.logs import logger
from entities.media import MediaType

MEDIA_TYPE_KEY_MAP = {
    kb_val.KEY_MOVIE_ADD: MediaType.MOVIE,
    kb_val.KEY_SERIES_ADD: MediaType.SERIES,
    kb_val.KEY_ANIME_ADD: MediaType.ANIME,
}


async def adding_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сообщение-ветка для добавления контента -> Выбор типа"""
    if update.message is None:
        return States.MAIN_MENU

    await update.message.reply_text(
        text="Что хотим добавить?",
        reply_markup=media.choosing_media_type(),
    )
    await update.message.delete()
    return States.CHOOSING_MEDIA_TYPE


async def get_media_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохранение выбранного типа -> Получение названия"""
    if update.callback_query is None:
        return States.MAIN_MENU
    if context.user_data is None:
        return States.MAIN_MENU

    query_data = update.callback_query.data or "_EMPTY_"
    media_type = MEDIA_TYPE_KEY_MAP.get(query_data, None)
    if media_type is None:
        logger.error(f"Unknown media type: {query_data}")
        return States.MAIN_MENU

    context.user_data["media_type"] = media_type

    if media_type is MediaType.MOVIE:
        msg_text = "Какой фильм добавляем?"
    elif media_type is MediaType.SERIES:
        msg_text = "Какой сериал добавляем?"
    elif media_type is MediaType.ANIME:
        msg_text = "Какое аниме добавляем?"
    else:
        msg_text = "Неизвестный тип контента."  # Should not happen

    await update.callback_query.edit_message_text(
        msg_text,
        reply_markup=None,
    )
    return States.SAVE_MEDIA


async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return States.MAIN_MENU
    if context.user_data is None:
        return States.MAIN_MENU
    if (title := getter.get_message_text(update.message)) is None:
        return States.MAIN_MENU

    # TODO FIX IT MOC
    user_id = 1
    await MediaService().add_media(
        media_data=NewMediaDTO(
            title=title,
            media_type=context.user_data["media_type"],
            user_id=user_id,
        )
    )
    if context.user_data["media_type"] == MediaType.MOVIE:
        msg_text = "✅ Фильм добавлен!"
    elif context.user_data["media_type"] == MediaType.SERIES:
        msg_text = "✅ Сериал добавлен!"
    else:
        msg_text = "✅ Аниме добавлено!"

    await update.message.reply_text(
        msg_text,
        reply_markup=base.main_menu(),
    )
    return States.MAIN_MENU


async def showing_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None:
        return States.MAIN_MENU

    # await update.message.reply_text(
    #     text="Что нужно найти?",
    #     # reply_markup=media.
    # elif context.user_data["media_type"] == MediaType.SERIES:
    #     msg_text = "✅ Сериал добавлен!"
    # else:
    #     msg_text = "✅ Аниме добавлено!"

    await update.callback_query.edit_message_text(
        "Введите название:",
        reply_markup=None,
    )
    return States.SAVE_MEDIA


async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return States.MAIN_MENU
    if context.user_data is None:
        return States.MAIN_MENU
    if (title := getter.get_message_text(update.message)) is None:
        return States.MAIN_MENU

    # TODO FIX IT MOC
    user_id = 1
    await MediaService().add_media(
        media_data=NewMediaDTO(
            title=title,
            media_type=context.user_data["media_type"],
            user_id=user_id,
        )
    )
    if context.user_data["media_type"] == MediaType.MOVIE:
        msg_text = "✅ Фильм добавлен!"
    elif context.user_data["media_type"] == MediaType.SERIES:
        msg_text = "✅ Сериал добавлен!"
    else:
        msg_text = "✅ Аниме добавлено!"

    await update.message.reply_text(
        msg_text,
        reply_markup=base.main_menu(),
    )
    return States.MAIN_MENU


async def showing_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None:
        return States.MAIN_MENU

    await update.message.reply_text(
        text="Что нужно найти?",
        reply_markup=media.media_type_menu(),
    )
    await update.message.delete()
    return States.START_SHOW_MEDIA


# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     if query is None:
#         return States.MAIN_MENU

#     await query.answer()
#     logger.debug(f"query.data: {query.data}")

#     if query.data == kb_val.KEY_ANIME_ADD:
#         await query.edit_message_text("Введите название:")
#         return States.START_ADD_MEDIA  # Переход в состояние добавления

#     if query.data == "list_media":
#         return await show_media_list(update, context, page=1)

#     if query.data == "filter_all":
#         return await show_media_list(update, context, page=1)


# async def add_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Обработчик добавления контента"""
#     if update.message is None:
#         return States.MAIN_MENU

#     if (user_id := get_user_id(update.message)) is None:
#         return States.MAIN_MENU
#     if (title := get_message_text(update.message)) is None:
#         return States.MAIN_MENU

#     # TODO FIX IT MOC
#     user_id = 1
#     await MediaService().add_media(
#         media_data=MediaDTO(
#             title=title,
#             media_type=MediaTypeEnum.MOVIE,
#             user_id=user_id,
#         )
#     )
#     await update.message.reply_text(
#         "✅ Запись добавлена!",
#         reply_markup=base.main_menu(),
#     )
#     return States.MAIN_MENU


# async def show_media_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1, watched_filter: str = None):
#     user_id = update.effective_user.id
#     context.user_data["current_page"] = page
#     context.user_data["current_filter"] = watched_filter
#     logger.debug(
#         f"user_id: {user_id}, page: {page}, watched_filter: {watched_filter}"
#     )
#     service = MediaService()

#     # Получаем записи с фильтрацией
#     media_items = await service.get_user_media(
#         user_id=user_id,
#         page=page,
#         watched_filter=watched_filter
#     )
#     total_items = await service.get_media_count(
#         user_id=user_id,
#         watched_filter=watched_filter  # TODO
#     )
#     total_pages = max(1, (total_items + 2) // 3)  # Округляем вверх

#     # Формируем текст сообщения
#     message_text = "🎬 Ваши записи:\n\n"
#     if watched_filter:
#         message_text += f"Фильтр: {'просмотренные' if watched_filter == 'watched' else 'не просмотренные'}\n\n"

#     for idx, item in enumerate(media_items, start=1):
#         status = "✅" if item.watched else "🟡"
#         message_text += f"{idx}. {status} {item.title}\n"

#     # Создаем клавиатуру
#     buttons = []

#     # Кнопки для каждой записи
#     for item in media_items:
#         buttons.extend(media.media_item_buttons(item.id, item.watched))

#     # Кнопки фильтрации
#     buttons.append([
#         InlineKeyboardButton(
#             text="Все",
#             callback_data="filter_all",
#         ),
#         InlineKeyboardButton(
#             text="Просмотренные",
#             callback_data="filter_watched",
#         ),
#         InlineKeyboardButton(
#             text="Не просмотренные",
#             callback_data="filter_unwatched",
#         )
#     ])

#     # Кнопки пагинации
#     if total_pages > 1:
#         nav_buttons = []
#         if page > 1:
#             nav_buttons.append(
#                 InlineKeyboardButton(
#                     text="⬅️ Назад", callback_data=f"page_{page-1}"))
#         if page < total_pages:
#             nav_buttons.append(InlineKeyboardButton(
#                 "Вперед ➡️", callback_data=f"page_{page+1}"))
#         buttons.append(nav_buttons)

#     # Кнопка возврата
#     buttons.append([InlineKeyboardButton(
#         "↩️ В меню", callback_data="main_menu")])

#     keyboard = InlineKeyboardMarkup(buttons)

#     # Отправка/обновление сообщения
#     if update.callback_query:
#         logger.info("123")
#         await update.callback_query.edit_message_text(
#             text=message_text,
#             reply_markup=keyboard
#         )
#     else:
#         logger.info("456")
#         await update.message.reply_text(
#             text=message_text,
#             reply_markup=keyboard
#         )

#     return States.VIEWING_LIST


# async def page_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     page = int(update.callback_query.data.split("_")[1])
#     return await show_media_list(update, context, page)


# async def toggle_watch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     media_id = int(update.callback_query.data.split("_")[2])
#     await MediaService().toggle_watched_status(media_id)

#     # Обновляем сообщение
#     current_page = context.user_data.get("current_page", 1)
#     return await show_media_list(update, context, current_page)
