
from telegram import Message, Update

def get_user_id(message: Message | None) -> int | None:
    if message is None:
        return None
    if message.from_user is None:
        return None
    return message.from_user.id


def get_message_text(message: Message | None) -> str | None:
    if message is None:
        return None
    return message.text
