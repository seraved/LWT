from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .constants import (
    KEY_ANIME,
    KEY_MOVIE,
    KEY_SERIES,
    KEY_ALL,
    KEY_RETURN_TO_SELECTION,
    ANIME_TEXT,
    FILM_TEXT,
    SERIES_TEXT,
    ALL_TYPE_TEXT,
)


def choosing_media_type(for_add=False):
    buttons = [
        InlineKeyboardButton(FILM_TEXT, callback_data=KEY_MOVIE),
        InlineKeyboardButton(SERIES_TEXT, callback_data=KEY_SERIES),
        InlineKeyboardButton(ANIME_TEXT, callback_data=KEY_ANIME),
    ]
    if for_add:
        return InlineKeyboardMarkup([
            buttons
        ])

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(ALL_TYPE_TEXT, callback_data=KEY_ALL),
        ],
        buttons,
    ])


def back_to_main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                "↩️ Назад", callback_data=KEY_RETURN_TO_SELECTION)],
        ]
    )


def media_list_keyboard(
    page: int,
    total_pages: int,
    parent_layer: list[InlineKeyboardButton] | None = None
) -> InlineKeyboardMarkup:
    """Клавиатура для пагинации"""
    buttons = []
    if total_pages > 1:
        nav_buttons = []
        if page > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"page_{page-1}",
                )
            )
        if page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="Вперед ➡️",
                    callback_data=f"page_{page+1}",
                )
            )
        buttons.append(nav_buttons)
    buttons.append([
        InlineKeyboardButton(
            text="↩️ В меню",
            callback_data=KEY_RETURN_TO_SELECTION
        )
    ])
    if parent_layer:
        return InlineKeyboardMarkup([
            parent_layer,
            *buttons
        ])
    return InlineKeyboardMarkup(buttons)


def media_item_buttons(media_id: int, is_watched: bool):
    return [
        [
            InlineKeyboardButton(
                text="✅ Просмотрено" if not is_watched else "👀 Не просмотрено",
                callback_data=f"toggle_watch_{media_id}"
            ),
            InlineKeyboardButton(
                text="✏️ Редактировать",
                callback_data=f"edit_{media_id}")
        ]
    ]
