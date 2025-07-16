from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import constants as const
from bot.keyboards import lwt as lwt_kb
from bot.states import LWTStates
from services.media import MediaService
from utils.logs import logger

from .common import content_media_builder
from entities.enum import WatchedEnum
from utils.mapper import key_to_media_type, key_to_text

router = Router()

BASE_TEXT = "Я LWT бот."


@router.message(F.text == const.SHOW_CONTENT_TEXT)
async def start_show_media(message: Message, state: FSMContext, **kwargs):
    """Сообщение-ветка для добавления контента -> Выбор типа"""

    await state.set_state(LWTStates.showing_media)

    await message.delete()
    await message.answer(
        text=(
            f"Всего записей: 10 \n"
            f"{const.ANIME_TEXT}: 1 \n"
            f"{const.MOVIE_TEXT}: 2 \n"
            f"{const.SERIES_TEXT}: 3 \n"
        ),
        reply_markup=lwt_kb.inl_filters_keyboard()
    )


@router.callback_query(
    LWTStates.showing_media,
    F.data.in_(
        (
            const.KEY_TYPE_ANIME, const.KEY_TYPE_MOVIE, const.KEY_TYPE_SERIES,
            const.KEY_ALL,
            const.KEY_IS_WATCHED, const.KEY_IS_UNWATCHED,
        )
    ),
)
async def get_filter(callback: CallbackQuery, state: FSMContext):
    """"""
    if callback.message is None:
        raise AiogramError("No Message")
    show_filter = await state.get_value("show_filter") or {}

    if callback.data in {const.KEY_TYPE_ANIME, const.KEY_TYPE_MOVIE, const.KEY_TYPE_SERIES}:
        show_filter["media_type"] = key_to_media_type(callback.data or "")
        show_filter["media_type_text"] = key_to_text(callback.data or "")
    if callback.data in {const.KEY_IS_WATCHED, const.KEY_IS_UNWATCHED}:
        if callback.data == const.KEY_IS_WATCHED:
            show_filter["watched"] = WatchedEnum.WATCHED
            show_filter["watched_text"] = "Только просмотренные"
        else:
            show_filter["watched"] = WatchedEnum.UNWATCHED
            show_filter["watched_text"] = "Только Не просмотренные"
    if callback.data == const.KEY_ALL:
        show_filter = {}

    await state.set_data(data={"show_filter": show_filter})

    await callback.message.edit_text(
        text=(
            f"Фильтры: \n"
            f" - Тип: {show_filter.get('media_type_text') or 'Все'}\n"
            f" - Просмотренные: {show_filter.get('watched_text') or 'Все'}\n"
        ),
        reply_markup=lwt_kb.inl_filters_keyboard()
    )


@router.callback_query(
    LWTStates.showing_media,
    F.data == const.KEY_APPLY_FILTER,
)
async def show_content(callback: CallbackQuery, state: FSMContext):
    """"""
    if callback.message is None:
        raise AiogramError("No Message")
    await state.set_state(LWTStates.list_content)

    show_filter = await state.get_value("show_filter") or {}
    user_id = callback.from_user.id or -1
    media_type = show_filter.get("media_type")
    watched = show_filter.get("watched")
    service = MediaService()
    total = await service.get_media_count(
        user_id=user_id,
        media_type=media_type,
        watched_filter=watched,
    )
    result = await service.get_user_media(
        user_id=user_id,
        media_type=media_type,
        watched_filter=watched,
        page=1,
        per_page=1,
    )
    if not result:
        await state.set_state(LWTStates.showing_media)
        await callback.message.edit_text(
            text=(
                "Нет данных\n"
                f"Фильтры: \n"
                f" - Тип: {show_filter.get('media_type_text') or 'Все'}\n"
                f" - Просмотренные: {show_filter.get('watched_text') or 'Все'}\n"
            ),
            reply_markup=lwt_kb.inl_filters_keyboard()
        )
        return
    content, *_ = result
    await callback.message.edit_media(
        media=content_media_builder(
            content=content,
            status=f"1 / {total}"
        ),
        reply_markup=lwt_kb.inl_show_content_pagination(
            page=0,
            total_pages=total,
            content=content,
        )
    )


@router.callback_query(
    LWTStates.list_content,
    F.data.startswith(const.PRE_KEY_PAGE)
)
async def list_content(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        raise AiogramError("No callback data")

    if callback.message is None:
        raise AiogramError("No callback message")

    page = int(callback.data.split("__")[1])

    show_filter = await state.get_value("show_filter") or {}
    user_id = callback.from_user.id or -1
    media_type = show_filter.get("media_type")

    service = MediaService()
    total = await service.get_media_count(
        user_id=user_id,
        media_type=media_type,
    )
    content, *_ = await service.get_user_media(
        user_id=user_id,
        media_type=media_type,
        page=page+1,
        per_page=1,
    )

    await callback.message.edit_media(
        media=content_media_builder(
            content=content,
            status=f"{page+1} / {total}"
        ),
        reply_markup=lwt_kb.inl_show_content_pagination(
            page=page,
            total_pages=total,
            content=content,
        )
    )


@router.callback_query(
    LWTStates.list_content,
    F.data.startswith(const.PRE_KEY_UPD_WATCHED)
)
async def set_watched_unwatched(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        raise AiogramError("No callback data")

    if callback.message is None:
        raise AiogramError("No callback message")

    page = int(callback.data.split("__")[1])

    show_filter = await state.get_value("show_filter") or {}
    user_id = callback.from_user.id or -1
    media_type = show_filter.get("media_type")

    service = MediaService()
    total = await service.get_media_count(
        user_id=user_id,
        media_type=media_type,
    )
    content, *_ = await service.get_user_media(
        user_id=user_id,
        media_type=media_type,
        page=page+1,
        per_page=1,
    )
    content = await service.toggle_watched_status(content.id)
    if content is None:
        raise AiogramError("No content after change watched flag")

    await callback.message.edit_media(
        media=content_media_builder(
            content=content,
            status=f"{page+1} / {total}"
        ),
        reply_markup=lwt_kb.inl_show_content_pagination(
            page=page,
            total_pages=total,
            content=content
        )
    )

# TODO feat: Добавить удаление
