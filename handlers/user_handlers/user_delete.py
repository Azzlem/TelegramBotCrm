from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from actions_base.actions_users import UserActions
from dataclass import DataClass
from keybords.keyboards import keyboard_list_user
from permission import is_owner
from states.states_user import FormDeleteUser

router = Router()


@router.message(Command(commands=["deluser"]))
async def del_user(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_owner(user):
        keyboard = await keyboard_list_user()
        await message.answer(text=" Выберите пользователя которого хотите удалить. ", reply_markup=keyboard)
        await state.set_state(FormDeleteUser.user_id)
    else:
        await message.answer(text="У вас не та это прав!")
        await state.clear()


@router.callback_query(StateFilter(FormDeleteUser.user_id),
                       F.data.in_([str(el) for el in range(1500)]))
async def del_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.data)
    await callback.message.delete()
    data = await state.get_data()
    await UserActions.delete_user(data)
    await callback.message.answer(
        f"Выбранный вами пользователь удалён."
    )
