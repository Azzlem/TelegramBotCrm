from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from keybords.keyboards import keyboard_choice_customer_filter, keyboard_list_user, keyboard_list_user_for_order
from permission import is_registered, is_owner_admin_user
from states.states_orders import FormAddOrder

router = Router()


@router.message(Command(commands=["order_add"]))
async def add_order(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_registered(user):
        await message.answer(text="Обратитсь к администратору за активацией вашего профиля")
    elif await is_owner_admin_user(user):
        await message.answer(text="Введите фамилию клиента или наименование организации")
        await state.set_state(FormAddOrder.fullname)


async def alpha_row(rows: str):
    row = []
    for el in rows.split():
        row.append(el.isalpha())
    return True if not False in row else False


@router.message(StateFilter(FormAddOrder.fullname))
async def add_order_customer(message: Message, state: FSMContext):
    if await alpha_row(message.text):
        keyboard = await keyboard_choice_customer_filter(message.text)
        if not keyboard:
            await message.answer(
                text=f"НЕТ ТАКОГО КЛИЕНТА!!!\n"
                     f"Если вы не нашли клиента, вы неверно ввели его имя,\n"
                     f"Нажмите /cancel,\nа после нажмите /order_add ещё раз,\nЕсли это не помогло, возможно "
                     f"клиента нет в базе данных,\nсоздайте клиента через команду /customer_add"
            )
            await state.clear()
        else:
            await message.answer(
                text=f"Выберите из существующих\n",
                reply_markup=keyboard
            )
        await state.set_state(FormAddOrder.customer_id)

    else:
        await message.answer("Это не похоже на имя и фамилию. Введи то что просят!")


@router.callback_query(StateFilter(FormAddOrder.customer_id))
async def add_order_user(callback: CallbackQuery, state: FSMContext):
    await state.update_data(customer_id=int(callback.data))
    keyboard = await keyboard_list_user_for_order(callback.from_user)
    await callback.message.delete()
    await callback.message.answer(
        text="Выберите инженера",
        reply_markup=keyboard
    )
    await state.set_state(FormAddOrder.user_id)


@router.callback_query(StateFilter(FormAddOrder.user_id))
async def add_order_price(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=int(callback.data))
    await callback.message.delete()
    data = await state.get_data()
    await OrdersActions.add_orders(data)
    await callback.message.answer(
        text="Успешно, поидее...."
    )
    await state.clear()
