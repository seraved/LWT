
from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    registration = State()
    awaiting_approval = State()


class LWTStates(AuthStates):
    home = State()

    adding_media = State()
    select_result = State()

    showing_media = State()
    list_content = State()
