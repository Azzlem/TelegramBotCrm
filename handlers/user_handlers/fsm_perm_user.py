from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from actions_base.actions_users import UserActions
from keybords.keyboards import keyboard_list_user, keyboard_list_orders
from states.states_user import FormChangePermsUser


router = Router()


@router.message(Command(commands=["change_perms"]))
async def change_perms_user(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if user.role.name in ["REGISTERED", "USER"]:
        await message.answer(
            text="У вас нет прав!"
        )
        await state.clear()
    elif user.role.name in ["OWNER", "ADMIN"]:
        users = await UserActions.get_all_users()
        keyboard = await keyboard_list_user()
        await message.answer(
            text=" Выберите пользователя которому хотите изменить права. ",
            reply_markup=keyboard
        )
        await state.set_state(FormChangePermsUser.user_id)
    else:
        await message.answer(
            text="Ты блять кто?"
        )
        await state.clear()


@router.callback_query(StateFilter(FormChangePermsUser.user_id),
                       F.data.in_([str(el) for el in range(1500)]))
async def change_perms_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.data)
    await callback.message.delete()
    keyboard = await keyboard_list_orders()
    await callback.message.answer(
        text="Выберите права пользователя.",
        reply_markup=keyboard
    )
    await state.set_state(FormChangePermsUser.role)


@router.callback_query(StateFilter(FormChangePermsUser.role),
                       F.data.in_(["REGISTERED", "USER", "ADMIN"]))
async def change_perms_user_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(role=callback.data)
    await callback.message.delete()
    data = await state.get_data()
    await UserActions.update_user(data)
    await callback.message.answer(
        text=f"Успешно.... поидее..."
    )
