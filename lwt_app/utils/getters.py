
from telegram import Message, Update


def get_user_id(message: Message | None) -> int | None:
    if message is None:
        return None
    if message.from_user is None:
        return None
    return message.from_user.id


def get_user_phone(message: Message | None) -> str | None:
    if message is None:
        return None
    if message.contact is None:
        return None
    return message.contact.phone_number


def get_user_fullname(message: Message | None) -> str | None:
    if message is None:
        return None
    if message.from_user is None:
        return None
    return message.from_user.full_name


def get_message_text(message: Message | None) -> str | None:
    if message is None:
        return None
    return message.text


def get_query_data(update: Update | None) -> str | None:
    if update is None:
        return None
    if update.callback_query is None:
        return None
    return update.callback_query.data
