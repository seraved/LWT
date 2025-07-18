from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import constants as const
from bot.keyboards import lwt as lwt_kb
from bot.states import LWTStates
from clients.kinopoisk import KinopoiskClient
from entities.media import FoundMediaContent, NewMediaDTO
from services.media import MediaService
from services.user import UserService
from utils.logs import logger

from .common import (
    content_media_builder,
    message_answer_founded_media,
    callback_message_edit_founded_media,
    get_statistic_msg,
)

router = Router()

BASE_TEXT = "Я LWT бот."


@router.message(F.text == const.ADD_CONTENT_TEXT)
async def start_add_media(message: Message, state: FSMContext, **kwargs):
    """Сообщение-ветка для добавления контента -> Выбор типа"""
    await state.set_state(LWTStates.adding_media)
    await message.delete()
    await message.answer(
        text="Что требуется найти?",
        reply_markup=lwt_kb.inl_back_to_home_state_keyboard()
    )


@router.message(
    LWTStates.adding_media,
    F.text.not_in((const.ADD_CONTENT_TEXT, const.SHOW_CONTENT_TEXT))
)
async def get_content_title(message: Message, state: FSMContext):
    """Получаем сообщение с названием и начнем поиск """
    title_name = message.text
    if title_name is None:
        raise AiogramError("Not content name")

    async with KinopoiskClient() as client:
        found_content = await client.search(title_name=title_name)

    if not found_content:
        await message.answer(
            text="Ничего не нашел, попробуй написать иначе",
            reply_markup=lwt_kb.inl_back_to_home_state_keyboard()
        )
        return

    await state.set_state(LWTStates.select_result)
    await state.update_data(data={"found_content": found_content})

    page = 0

    await message_answer_founded_media(
        message=message,
        found_content=found_content[page],
        page=page,
        total_pages=len(found_content),
        reply_markup=lwt_kb.inl_found_content_pagination(
            page=page,
            total_pages=len(found_content),
        )
    )


@router.callback_query(
    F.data == const.KEY_TO_HONE_TYPE,
    LWTStates.adding_media,
)
async def go_back_to_home(callback: CallbackQuery, state: FSMContext):
    """Откат -> главное меню"""
    if (message := callback.message) is None:
        raise AiogramError("No Message")

    await state.set_data(data={"title": None})

    user_id = callback.from_user.id or -1

    await message.delete_reply_markup()

    await message.edit_text(
        text=await get_statistic_msg(user_id=user_id)
    )

    await state.set_state(LWTStates.home)


@router.callback_query(
    LWTStates.select_result,
    F.data.startswith(const.PRE_KEY_PAGE)
)
async def list_founded_values(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        raise AiogramError("No callback data")

    if callback.message is None:
        raise AiogramError("No callback message")

    found_content = await state.get_value("found_content")
    if found_content is None:
        raise AiogramError("Pagination no content")

    page = int(callback.data.split("__")[1])
    # TODO feat: кнопка Вернуться и поискать другое
    await callback_message_edit_founded_media(
        message=callback.message,
        found_content=found_content[page],
        page=page,
        total_pages=len(found_content),
        reply_markup=lwt_kb.inl_found_content_pagination(
            page=page,
            total_pages=len(found_content),
        )
    )
    await callback.answer()


@router.callback_query(
    LWTStates.select_result,
    F.data.startswith(const.PRE_KEY_SELECTED)
)
async def select_found_value(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        raise AiogramError("No callback data")

    if callback.message is None:
        raise AiogramError("No callback message")

    found_content = await state.get_value("found_content")
    if found_content is None:
        raise AiogramError("Pagination no content")

    user = await state.get_value("user")
    if user is None:
        user = await UserService().get_user(user_id=callback.from_user.id)
        if user is None:
            raise AiogramError("No User")

    idx = int(callback.data.split("__")[1])
    content = found_content[idx]

    await MediaService().add_media_content(
        user=user,
        media_content=NewMediaDTO.from_found_content(content)
    )
    await callback.message.delete_reply_markup()
    await callback.message.edit_media(
        media=content_media_builder(
            content=content,
            status=const.ADDED_TEXT,
        ),
    )
    await state.update_data(data={"found_content": None})
    found_content = await state.get_value("found_content")
    # TODO feat: Добавить сообщение о успехе и открыть клавиатуру (например сколько фильмов добавлено\просмотрено)
    await state.set_state(LWTStates.home)
    await callback.answer()
