

from telegram.ext import ContextTypes
from telegram import Update
from bot.states import States
from bot.keyboards import base

from utils import getters as getter
from utils.logs import logger


async def auth_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик авторизации пользователя"""
    logger.debug("auth_user")
    if update.message is None:
        return States.START_MENU

    if (user_id := getter.get_user_id(update.message)) is None:
        return States.START_MENU

    if (phone := getter.get_user_phone(update.message)) is None:
        return States.START_MENU

    logger.debug(f"user_id: {user_id}, phone: {phone}")

    # найти пользователя
    if user_id == 404663374 and phone == "+79535412847":
        full_name = getter.get_user_fullname(update.message) or "Аноним"
        await update.message.reply_text(
            f"👋 Привет {full_name}!",
            reply_markup=base.main_menu(),
        )
        return States.MAIN_MENU

    await update.message.reply_text(
        "Тебе тут не рады. Уходи!",
    )
    return States.START_MENU
    # вывести главное меню

    # if (title := get_message_text(update.message)) is None:
    #     return States.MAIN_MENU

    # # TODO FIX IT MOC
    # user_id = 1
    # await MediaService().add_media(
    #     media_data=MediaDTO(
    #         title=title,
    #         media_type=MediaTypeEnum.MOVIE,
    #         user_id=user_id,
    #     )
    # )
    # await update.message.reply_text(
    #     "✅ Запись добавлена!",
    #     reply_markup=base.main_menu(),
    # )
    return States.MAIN_MENU
