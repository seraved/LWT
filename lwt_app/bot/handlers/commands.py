from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import auth as auth_kb
from bot.keyboards import lwt as lwt_kb
from bot.states import LWTStates
from services.user import UserService

from .common import get_statistic_msg

router = Router()


# Стартовая команда
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    """Обработки стартовой команды /start

        Проверят разрешено ли пользователю использовать бота
        ЕСЛИ: разрешено: открываем основное меню бота
        ЕСЛИ: на рассмотрении: Выводим об этом сообщение и выводим кнопку проверить еще раз
        Иначе: Предлагаем зарегистрироваться
    """

    user_id = message.from_user.id if message.from_user else -1

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
        await state.set_data(data={"user": user})

        stat_msg = await get_statistic_msg(user_id=user_id)
        await message.answer(
            text=f"Привет! {user.full_name}! \n\n {stat_msg}",
            reply_markup=lwt_kb.rep_lwt_home_keyboard()
        )
        return

    await state.set_state(LWTStates.awaiting_approval)
    await message.answer(
        text="Ваша заявка на рассмотрении, Попробуй позднее",
        reply_markup=auth_kb.check_approval_keyboard())
