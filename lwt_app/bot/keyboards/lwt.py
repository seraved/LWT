from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import constants as const
from entities.media import MediaDTO


from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# Reply-кнопки


def rep_lwt_home_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=const.ADD_CONTENT_TEXT),
                KeyboardButton(text=const.SHOW_CONTENT_TEXT),
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        selective=True,
    )


def rep_empty_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[],
        resize_keyboard=True,
    )

# Inline-кнопки


def inl_found_content_pagination(
    page: int = 0,
    total_pages: int = 1,
):
    pagination: list[InlineKeyboardButton] = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton(
                text=const.PAGE_BACK_TEXT,
                callback_data=f"{const.PRE_KEY_PAGE}{page-1}"),
        )
    if total_pages > (page+1):
        pagination.append(
            InlineKeyboardButton(
                text=const.PAGE_FORWARD_TEXT,
                callback_data=f"{const.PRE_KEY_PAGE}{page+1}"
            ),
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=const.PAGE_SELECT_TEXT,
                callback_data=f"{const.PRE_KEY_SELECTED}{page}"
            )],
            pagination,
        ]
    )


def inl_back_to_home_state_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=const.BACK_TEXT,
                    callback_data=const.KEY_TO_HONE_TYPE,
                ),
            ],
        ]
    )


def inl_filters_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=const.MOVIE_TEXT,
                callback_data=const.KEY_TYPE_MOVIE,
            ),
            InlineKeyboardButton(
                text=const.SERIES_TEXT,
                callback_data=const.KEY_TYPE_SERIES,
            ),
            InlineKeyboardButton(
                text=const.ANIME_TEXT,
                callback_data=const.KEY_TYPE_ANIME,
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.WATCHED_TEXT,
                callback_data=const.KEY_IS_WATCHED,
            ),
            InlineKeyboardButton(
                text=const.UNWATCHED_TEXT,
                callback_data=const.KEY_IS_UNWATCHED,
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.ALL_TYPE_TEXT,
                callback_data=const.KEY_ALL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=const.APPLY_FILTER_TEXT,
                callback_data=const.KEY_APPLY_FILTER,
            ),
        ]
    ])


def inl_show_content_pagination(
    content: MediaDTO,
    page: int = 0,
    total_pages: int = 1,
):
    pagination: list[InlineKeyboardButton] = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton(
                text=const.PAGE_BACK_TEXT,
                callback_data=f"{const.PRE_KEY_PAGE}{page-1}"),
        )
    if total_pages > (page+1):
        pagination.append(
            InlineKeyboardButton(
                text=const.PAGE_FORWARD_TEXT,
                callback_data=f"{const.PRE_KEY_PAGE}{page+1}"
            ),
        )
    key_text = const.PAGE_SET_UNWATCHED if content.watched else const.PAGE_SET_WATCHED
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=key_text,
                callback_data=f"{const.PRE_KEY_UPD_WATCHED}{page}"
            )],
            pagination,
        ]
    )


def inl_empty_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[])
