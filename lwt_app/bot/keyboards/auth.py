from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.keyboards import constants as const

# Reply-кнопки


def auth_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=const.REGISTRATION_TEXT,
                    request_contact=True,
                )
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# Inline-кнопки
def check_approval_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=const.CHECK_APP_AGAIN_TEXT,
                    callback_data=const.KEY_CHECK_APP_TEXT,
                )
            ],
        ],
    )
