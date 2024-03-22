from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from actions_base.actions_users import UserActions
from formatting.user_formatting import DataObject
from keybords.keyboards import keyboard_list_user
from permission import is_owner_admin
from states.states_user import FormDetailUser

router = Router()


@router.message(Command(commands=["listuser"]))
async def list_user(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_owner_admin(user):
        keyboard = await keyboard_list_user()
        await message.answer(
            text=" Выберите пользователя.",
            reply_markup=keyboard
        )
        await state.set_state(FormDetailUser.user_id)
    else:
        await message.answer(text="У вас нет на это прав")
        await state.clear()


@router.callback_query(StateFilter(FormDetailUser.user_id),
                       F.data.in_([str(el) for el in range(1500)]))
async def detail_user(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.data)
    await callback.message.delete()
    data = await state.get_data()
    data = DataObject(data=data)
    user = await UserActions.get_user_from_id(data)
    await callback.message.answer(
        f"ФИО: {user.fullname}\nПрава: {user.role.name}\n"
        f"Никнэйм: {user.username}\nРаботает с {user.created_on.strftime('%d-%m-%Y')}\n"
    )
