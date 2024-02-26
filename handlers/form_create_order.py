from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from OrderActionsBase import OrderService
from UserActionsBase import UserService
from keybords.keyboards import keyboard_create_orders_user, keyboard_create_orders_users

from states.states import FormOrder

router = Router()


@router.message(Command('order'))
async def command_order(message: Message, state: FSMContext):
    if await UserService.valid_user(message.from_user.id) in ['admin', 'user']:
        await state.set_state(FormOrder.client_name)
        await message.answer(
            f"Введи имя клиента"
        )
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@router.message(FormOrder.client_name)
async def command_client_name(message: Message, state: FSMContext):
    row = []
    for el in message.text.split():
        row.append(el.isalpha())
    if not False in row:
        await state.update_data(client_name=message.text)
        await state.set_state(FormOrder.client_phone)
        await message.answer(
            f"Введи телефон клиента"
        )
    else:
        await message.answer("Это не похоже на имя, введи имя не еби мозги!")


@router.message(FormOrder.client_phone)
async def command_client_phone(message: Message, state: FSMContext):
    if len(message.text) == 11 or len(message.text) == 7:
        await state.update_data(client_phone=message.text)
        await state.set_state(FormOrder.device)
        await message.answer(
            f"Введи вендор и модель техники."
        )
    else:
        await message.answer("Ты правда думаешь что если на отъебись заполнять форму то ты станешь миллионером?")


@router.message(FormOrder.device)
async def command_device(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrder.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@router.message(FormOrder.mulfunction)
async def command_mulfunction(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    if await UserService.valid_user(message.from_user.id) in ["admin"]:
        keyboard = await keyboard_create_orders_users()
    else:
        keyboard = await keyboard_create_orders_user(message.from_user)
    await message.answer(
        text='Выберите инженера!',
        reply_markup=keyboard
    )
    await state.set_state(FormOrder.user_id)


@router.callback_query(StateFilter(FormOrder.user_id),
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

