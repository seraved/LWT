from aiogram import F, Router, Bot
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, FSInputFile

from bot.keyboards import lwt as lwt_kb
from bot.keyboards import constants as const
from bot.states import LWTStates
from entities.media import NewMediaDTO, FoundMediaContent
from services.user import UserService
from services.media import MediaService
from utils.logs import logger
from clients.kinopoisk import KinopoiskClient
router = Router()

BASE_TEXT = "Я LWT бот."


@router.message(F.text == const.ADD_CONTENT_TEXT)
async def start_add_media(message: Message, state: FSMContext, **kwargs):
    """Сообщение-ветка для добавления контента -> Выбор типа"""
    await state.set_state(LWTStates.get_title)
    await message.delete()
    await message.answer(
        text="Что требуется найти?",
        reply_markup=lwt_kb.inl_back_to_home_state()
    )


def _create_media(content: FoundMediaContent, status: str = "") -> InputMediaPhoto:
    caption = (
        f"{status}\n"
        f"<b>{content.name}</b> ({content.year})\n"
        f"<b>Тип</b>: {content.media_type}\n"
        f"<b>Жанр</b>: {content.genres}\n"
        f"\n{content.description}"
    )
    if content.poster_url:
        return InputMediaPhoto(
            media=content.poster_url,
            caption=f"{caption[:1000]} ...",
            parse_mode="HTML",
        )
    return InputMediaPhoto(
        media=FSInputFile("lwt_app/bot/img/media_img_plug.png"),
        caption=f"{caption[:1000]} ...",
        parse_mode="HTML",
    )


@router.message(
    LWTStates.get_title,
    F.text.not_in((const.ADD_CONTENT_TEXT, const.SHOW_CONTENT_TEXT))
)
async def get_content_title(message: Message, state: FSMContext,  bot: Bot):
    """Получаем сообщение с названием и начнем поиск """
    title_name = message.text
    if title_name is None:
        raise AiogramError("Not content name")

    async with KinopoiskClient() as client:
        found_content = await client.search(title_name=title_name)

    if not found_content:
        await message.answer(
            text="Ничего не нашел, попробуй написать иначе",
            reply_markup=lwt_kb.inl_back_to_home_state()
        )
        return

    await state.set_state(LWTStates.select_result)
    await state.update_data(data={"found_content": found_content})

    page = 0

    message_media, *_ = await message.answer_media_group(
        media=[
            _create_media(
                content=found_content[page],
                status=f"{page +1} / {len(found_content)}"
            )
        ],
    )
    await message_media.edit_reply_markup(
        reply_markup=lwt_kb.inl_found_content_pagination(
            page=page,
            total_pages=len(found_content),
        )
    )


@router.callback_query(
    F.data == const.KEY_TO_HONE_TYPE,
    LWTStates.get_title,
)
async def go_back_to_home(callback: CallbackQuery, state: FSMContext):
    """Откат -> главное меню"""
    if (message := callback.message) is None:
        raise AiogramError("No Message")

    await state.set_data(data={"title": None})

    await message.edit_text(
        text=BASE_TEXT,
        reply_markup=lwt_kb.inl_empty_keyboard()
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
    await callback.message.edit_media(
        media=_create_media(
            content=found_content[page],
            status=f"{page +1} / {len(found_content)}"
        ),
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
    await callback.message.edit_media(
        media=_create_media(
            content=content,
            status=const.ADDED_TEXT,
        ),
        reply_markup=lwt_kb.inl_empty_keyboard()
    )
    await state.update_data(data={"found_content": None})
    found_content = await state.get_value("found_content")
    # TODO feat: Добавить сообщение о успехе и открыть клавиатуру (например сколько фильмов добавлено\просмотрено)
    await state.set_state(LWTStates.home)
    await callback.answer()
