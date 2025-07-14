from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .constants import KEY_ANIME, KEY_MOVIE, KEY_SERIES, KEY_RETURN_TO_SELECTION


def choosing_media_type():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 Фильм", callback_data=KEY_MOVIE),
            InlineKeyboardButton("📺 Сериал", callback_data=KEY_SERIES),
            InlineKeyboardButton("🇯🇵 Аниме", callback_data=KEY_ANIME),
        ],
    ])


def back_to_main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                "↩️ Назад", callback_data=KEY_RETURN_TO_SELECTION)],
        ]
    )


def media_list_keyboard(page: int, total_pages: int):
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
