from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import auth as auth_kb
from bot.keyboards import lwt as lwt_kb
from bot.keyboards import constants as const
from bot.states import LWTStates
from entities.user import NewUserDTO
from services.user import UserService
from utils.logs import logger

router = Router()

# Добавление задачи
ANONYM = "Anonymous"


@router.message(LWTStates.registration, F.contact)
async def registration(message: Message, state: FSMContext):
    """Обработка регистрации заявки на доступ к боту

        Получаем контакт и создаем пользователя
        После успешной регистрации заявка нуждается в подтверждении
    """
    try:
        contact = message.contact
        if contact is None:
            raise AiogramError("No Contact")
        if contact.user_id is None:
            raise AiogramError("No User ID")
        if message.from_user is None:
            raise AiogramError("No User")

        user_data = NewUserDTO(
            user_id=contact.user_id,
            username=message.from_user.username or ANONYM,
            full_name=" ".join(
                filter(None, [contact.last_name, contact.first_name])
            ),
            phone=contact.phone_number,
        )

        await UserService().create_user(user_data=user_data)
    except AiogramError as e:
        logger.exception(
            msg=f"Не удалось создать пользователя {str(user_data)}",
            exc_info=True,
        )

    await state.set_state(LWTStates.awaiting_approval)
    await message.answer(
        text="Ваша заявка добавлена в очередь на рассмотрение, Попробуй позднее",
        reply_markup=auth_kb.check_approval_keyboard()
    )


@router.callback_query(
    F.data.startswith(const.KEY_CHECK_APP_TEXT),
    LWTStates.awaiting_approval,
)
async def check_approval(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    attempt = state_data.get("attempt", 1)

    if (message := callback.message) is None:
        raise AiogramError("No Message")

    user_id = callback.from_user.id if callback.from_user else -1

    user = await UserService().get_user(user_id=user_id)
    if user is None:
        await state.set_state(LWTStates.registration)
        await message.answer(
            "Для доступа к боту подайте заявку администратору",
            reply_markup=auth_kb.auth_keyboard(),
        )
        return

    if user.is_approved:
        await state.set_state(LWTStates.home)
        await message.answer(
            f"Привет! {user.full_name}!",
            reply_markup=lwt_kb.rep_lwt_home_keyboard()
        )
        return

    state_data.update({"attempt": attempt + 1})
    await state.update_data(state_data)
    # TODO feat: Добавить ограничение проверок в день до 10
    await message.edit_text(
        text=f"Ваша заявка на рассмотрении, Попробуй позднее {attempt if attempt else ''}",
        reply_markup=auth_kb.check_approval_keyboard(),
    )
