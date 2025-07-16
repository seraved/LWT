from aiogram.types import InputMediaPhoto, FSInputFile

from entities.media import FoundMediaContent
from utils.logs import logger

from entities.media import MediaDTO


def content_media_builder(
    content: FoundMediaContent | MediaDTO,
    status: str = "",
) -> InputMediaPhoto:
    caption = f"{status}\n{content.to_msg()}"
    if content.poster_url:
        return InputMediaPhoto(
            media=content.poster_url,
            caption=f"{caption[:1010]} ...",
            parse_mode="HTML",
        )
    return InputMediaPhoto(
        media=FSInputFile("lwt_app/bot/img/media_img_plug.png"),
        caption=f"{caption[:1000]} ...",
        parse_mode="HTML",
    )
