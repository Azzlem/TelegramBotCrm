from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import keyboard_change_order_orders, keyboard_create_order_user
from service import Service
from utils_format import format_data_order_get
from states.states import FormOrderChange

router_order_change = Router()


@router_order_change.message(Command(commands=['change_order']))
async def change_order(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ['admin', 'user']:
        keyboard = await keyboard_change_order_orders()
        await message.answer(
            text="Введите номер заказа",
            reply_markup=keyboard
        )
        await state.set_state(FormOrderChange.order_id)
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@router_order_change.callback_query(StateFilter(FormOrderChange.order_id),
                                    F.data.in_([str(el) for el in range(1500)]))
async def change_order_callback_query(callback: CallbackQuery, state: FSMContext):
    await state.update_data(order_id=int(callback.data))
    await callback.message.delete()
    keyboard = await keyboard_create_order_user()
    print(keyboard)
    await callback.message.answer(
        text='Выберите инженера!',
        reply_markup=keyboard
    )
    await state.set_state(FormOrderChange.user_id)


@router_order_change.callback_query(StateFilter(FormOrderChange.user_id),
                                    F.data.in_([str(el) for el in range(15)]))
async def change_order_callback_user_query(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=int(callback.data))
    await callback.message.delete()

    await callback.message.answer(
        f"Введи новое имя клиента"
    )
    await state.set_state(FormOrderChange.client_name)


# @router_order_change.message(FormOrderChange.order_id)
# async def change_order_id(message: Message, state: FSMContext):
#     await state.update_data(id_order=message.text)
#     await state.set_state(FormOrderChange.user_id)
#     await message.answer(
#         f"Введи новый айди манагера\n\n\n"
#     )
#
#
# @router_order_change.message(FormOrderChange.user_id)
# async def change_user_id(message: Message, state: FSMContext):
#     await state.update_data(user_id=message.text)
#     await state.set_state(FormOrderChange.client_name)
#     await message.answer(
#         f"Введи новое имя клиента"
#     )
#
#
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
