from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Добавить запись", callback_data="add_media")],
        [InlineKeyboardButton("📋 Мои записи", callback_data="list_media")]
    ])


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
    buttons.append([InlineKeyboardButton(
        "↩️ В меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)
