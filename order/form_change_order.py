from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import keyboard_change_order_orders
from service import Service
from utils_format import format_data_order_get
from states.states import FormOrderChange

router_order_change = Router()


@router_order_change.message(Command(commands=['change_order']))
async def change_order(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ['admin', 'user']:
        keyboard = await keyboard_change_order_orders()
        await state.set_state(FormOrderChange.order_id)
        await message.answer(
            text="Введите номер заказа",
            reply_markup=keyboard
        )
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@router_order_change.message(FormOrderChange.order_id)
async def change_order_id(message: Message, state: FSMContext):
    await state.update_data(id_order=message.text)
    await state.set_state(FormOrderChange.user_id)
    await message.answer(
        f"Введи новый айди манагера\n\n\n"
    )


@router_order_change.message(FormOrderChange.user_id)
async def change_user_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(FormOrderChange.client_name)
    await message.answer(
        f"Введи новое имя клиента"
    )


@router_order_change.message(FormOrderChange.client_name)
async def change_client_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(FormOrderChange.client_phone)
    await message.answer(
        f"Введи новый телефон клиента"
    )


@router_order_change.message(FormOrderChange.client_phone)
async def change_client_phone(message: Message, state: FSMContext):
    await state.update_data(client_phone=message.text)
    await state.set_state(FormOrderChange.device)
    await message.answer(
        f"Введи вендор и модель техники."
    )


@router_order_change.message(FormOrderChange.device)
async def change_device(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrderChange.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@router_order_change.message(FormOrderChange.mulfunction)
async def change_mulfunction(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    data = await state.get_data()
    await Service.update_order(data)
    await message.answer(
        f"Заявка на ремонт\n{data['client_name']}\nуспешно изменена"
    )
    await state.clear()
