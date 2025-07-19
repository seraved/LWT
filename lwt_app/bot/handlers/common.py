from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    MaybeInaccessibleMessageUnion,
    Message
)
from bot.keyboards import constants as const
from entities.media import FoundMediaContent, MediaDTO
from services.media import MediaService
from utils.logs import logger


def content_media_builder(
    content: FoundMediaContent | MediaDTO,
    status: str = "",
    use_local_media: bool = False
) -> InputMediaPhoto:
    caption = f"{status}\n{content.to_msg()}"

    if not content.poster_url or use_local_media:
        return InputMediaPhoto(
            media=FSInputFile("lwt_app/bot/img/media_img_plug.png"),
            caption=f"{caption[:1000]} ...",
            parse_mode="HTML",
        )
    return InputMediaPhoto(
        media=content.poster_url,
        caption=f"{caption[:1000]} ...",
        parse_mode="HTML",
    )


async def message_answer_founded_media(
    message: Message,
    found_content: FoundMediaContent,
    page: int = 1,
    total_pages: int = 1,
    reply_markup: InlineKeyboardMarkup | None = None
):
    try:
        message_media, *_ = await message.answer_media_group(
            media=[
                content_media_builder(
                    content=found_content,
                    status=f"{page +1} / {total_pages}"
                )
            ],
        )
    except TelegramBadRequest as e:
        message_media, *_ = await message.answer_media_group(
            media=[
                content_media_builder(
                    content=found_content,
                    status=f"{page +1} / {total_pages}",
                    use_local_media=True,
                )
            ],
        )
    if reply_markup:
        await message_media.edit_reply_markup(
            reply_markup=reply_markup,
            page=page,
            total_pages=total_pages,
        )


async def callback_message_edit_media(
    message: MaybeInaccessibleMessageUnion,
    content: FoundMediaContent | MediaDTO,
    status: str | None = None,
    page: int = 1,
    total_pages: int = 1,
    reply_markup: InlineKeyboardMarkup | None = None
):
    try:
        await message.edit_media(
            media=content_media_builder(
                content=content,
                status=status or f"{page +1} / {total_pages}"
            ),
            reply_markup=reply_markup,
        )
    except Exception as e:
        await message.edit_media(
            media=content_media_builder(
                content=content,
                status=status or f"{page +1} / {total_pages}",
                use_local_media=True,
            ),
            reply_markup=reply_markup,
        )


async def get_statistic_msg(user_id: int) -> str:
    media_stats = await MediaService().get_statistic(user_id)
    return (
        f"Всего записей: {media_stats.total_cnt} \n"
        f"{const.ANIME_TEXT}: {media_stats.anime_cnt} \n"
        f"{const.MOVIE_TEXT}: {media_stats.movie_cnt} \n"
        f"{const.SERIES_TEXT}: {media_stats.series_cnt} \n"
    )
