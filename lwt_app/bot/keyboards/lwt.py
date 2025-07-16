from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.keyboards import constants as const


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


def content_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=const.FILM_TEXT,
                    callback_data=const.KEY_MOVIE,
                ),
                InlineKeyboardButton(
                    text=const.SERIES_TEXT,
                    callback_data=const.KEY_SERIES,
                ),
                InlineKeyboardButton(
                    text=const.ANIME_TEXT,
                    callback_data=const.KEY_ANIME,
                ),
            ],
        ],
    )


def inl_back_to_home_state():
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


def inl_empty_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[])
