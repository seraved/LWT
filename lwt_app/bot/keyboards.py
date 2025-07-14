from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Добавить запись", callback_data="add_media")],
        [InlineKeyboardButton("📋 Мои записи", callback_data="list_media")]
    ])
