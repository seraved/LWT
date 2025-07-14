from enum import IntEnum, auto


class States(IntEnum):
    START_MENU = auto()  # Основное меню входа
    MAIN_MENU = auto()  # Основное меню

    CHOOSING_MEDIA_TYPE = auto()
    SAVE_MEDIA = auto()

    START_SHOW_MEDIA = auto()
    SHOW_MEDIA = auto()


    # SHOW_MEDIA = auto()
    # EDIT_MEDIA = auto()
    # VIEWING_LIST = auto()
