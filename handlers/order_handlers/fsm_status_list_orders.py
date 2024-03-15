from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from keybords.keyboard_list_orders import keyboard_list_orders_status, keyboard_list_order_details, \
    keyboard_list_order_details_another_var
from models.enums import Status
from permission import is_registered, is_owner_admin_user, is_owner_admin, is_user
from states.states_orders import FormListOrderForStatus

router = Router()


@router.message(Command(commands=["list"]))
async def create_order(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_registered(user):
        await message.answer(text="Обратитсь к администратору за активацией вашего профиля")
    elif await is_owner_admin_user(user):
        keyboard = await keyboard_list_orders_status()
        await message.answer(text="ВЫБРАТЬ СТАТУС ЗАКАЗА?", reply_markup=keyboard)
        await state.set_state(FormListOrderForStatus.choise_status)
        await state.update_data(user=user)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_status), F.data.in_([status.name for status in Status]))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status=callback.data)
    await callback.message.delete()
    data = await state.get_data()


    user = data['user']
    status = data['status']

    if await is_owner_admin(user):
        user = None
        orders = await OrdersActions.get_all_orders_accepted(user, status)
        keyboard, text = await keyboard_list_order_details_another_var(orders)
        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )
        if text == "Нет заказов":
            await state.clear()
        else:
            await state.set_state(FormListOrderForStatus.order)
    elif await is_user(user):
        orders = await OrdersActions.get_all_orders_accepted(user, status)
        keyboard, text = await keyboard_list_order_details_another_var(orders)
        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )
        if text == "Нет заказов":
            await state.clear()
        else:
            await state.set_state(FormListOrderForStatus.order)


