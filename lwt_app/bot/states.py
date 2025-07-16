
from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    registration = State()
    awaiting_approval = State()


class LWTStates(AuthStates):
    # TODO TASK: Убрать лишние 
    home = State()
    # Добавить - выбрать тип - получить название - найти на кинопоиске - утвердить - сохранить - домой
    adding_media = State()
    select_media_type = State()
    get_title = State()
    select_result = State()
    approval_media = State()
    save_media = State()

    #
    showing_media = State()
