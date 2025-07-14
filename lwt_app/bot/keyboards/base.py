from telegram import KeyboardButton, ReplyKeyboardMarkup
from .constants import AUTH_BTN_TEXT, ADD_CONTENT_TEXT, SHOW_CONTENT_TEXT


def unauth_keyboard():
    """Клавиатура для авторизации"""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(AUTH_BTN_TEXT, request_contact=True)],
        ],
        resize_keyboard=True
    )


def main_menu():
    """Клавиатура для главного меню"""
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(ADD_CONTENT_TEXT),
                KeyboardButton(SHOW_CONTENT_TEXT),
            ]
        ],
        resize_keyboard=True
    )
