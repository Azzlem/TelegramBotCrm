from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from OrderActionsBase import OrderService
from keyboards import keyboard_create_order_user
from service import Service
from states.states import FormOrder

router_order_create = Router()


@router_order_create.message(Command('order'))
async def command_order(message: Message, state: FSMContext):
    await state.set_state(FormOrder.client_name)
    await message.answer(
        f"Введи имя клиента"
    )


@router_order_create.message(FormOrder.client_name)
async def command_client_name(message: Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(client_name=message.text)
        await state.set_state(FormOrder.client_phone)
        await message.answer(
            f"Введи телефон клиента"
        )
    else:
        await message.answer("Это не похоже на имя, введи имя не еби мозги!")


@router_order_create.message(FormOrder.client_phone)
async def command_client_phone(message: Message, state: FSMContext):
    if len(message.text) == 11 or len(message.text) == 7:
        await state.update_data(client_phone=message.text)
        await state.set_state(FormOrder.device)
        await message.answer(
            f"Введи вендор и модель техники."
        )
    else:
        await message.answer("Ты правда думаешь что если на отъебись заполнять форму то ты станешь миллионером?")


@router_order_create.message(FormOrder.device)
async def command_device(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrder.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@router_order_create.message(FormOrder.mulfunction)
async def command_mulfunction(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    keyboard = await keyboard_create_order_user()
    await message.answer(
        text='Выберите инженера!',
        reply_markup=keyboard
    )
    await state.set_state(FormOrder.user_id)


@router_order_create.callback_query(StateFilter(FormOrder.user_id),
                                    F.data.in_([str(el) for el in range(15)]))
async def command_user_id(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=int(callback.data))
    data = await state.get_data()
    await OrderService.create_order(data)
    await callback.message.delete()
    await callback.message.answer(
        text='Спасибо! Заказ успешно создан!\nЧто б просмотреть свои заказы наберите\n/list_orders'
    )
    await state.clear()

#     users = await Service.get_all_users()
#     print(users[0].name)
#     male_button = InlineKeyboardButton(
#         text=users[0].name,
#         callback_data='male'
#     )

# @router_order_create.callback_query(StateFilter(FormOrder.fill_gender),
#                    F.data.in_(['male', 'female', 'undefined_gender']))
# if message.text.isdigit() and 1 <= int(message.text) <= users[1]:
#     await state.update_data(user_id=int(message.text))
#     data = await state.get_data()
#     await OrderService.create_order(data)
#     await message.answer(
#         f"Заявка на ремонт \n{data['client_name']}\nуспешно создана"
#     )
#     await state.clear()
# else:
#     await message.answer("Вы ввели что то не то, введите верное значение!")
