from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from OrderActionsBase import OrderService
from service import Service
from states.states import FormOrder


router_order_create = Router()


@router_order_create.message(Command('order'))
async def command_name(message: Message, state: FSMContext):
    await state.set_state(FormOrder.client_name)
    await message.answer(
        f"Введи имя клиента"
    )


@router_order_create.message(FormOrder.client_name)
async def command_name(message: Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(client_name=message.text)
        await state.set_state(FormOrder.client_phone)
        await message.answer(
            f"Введи телефон клиента"
        )
    else:
        await message.answer("Это не похоже на имя, введи имя не еби мозги!")


@router_order_create.message(FormOrder.client_phone)
async def command_name(message: Message, state: FSMContext):
    if len(message.text) == 11 or len(message.text) == 7:
        await state.update_data(client_phone=message.text)
        await state.set_state(FormOrder.device)
        await message.answer(
            f"Введи вендор и модель техники."
        )
    else:
        await message.answer("Ты правда думаешь что если на отъебись заполнять форму то ты станешь миллионером?")


@router_order_create.message(FormOrder.device)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrder.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@router_order_create.message(FormOrder.mulfunction)
async def command_age(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    await state.set_state(FormOrder.user_id)
    users = await Service.get_all_users()
    await message.answer(users[0])
    await message.answer(
        "Введи айди манагера",
    )


@router_order_create.message(FormOrder.user_id)
async def command_name(message: Message, state: FSMContext):
    users = await Service.get_all_users()
    if message.text.isdigit() and 1 <= int(message.text) <= users[1]:
        await state.update_data(user_id=int(message.text))
        data = await state.get_data()
        await OrderService.create_order(data)
        await message.answer(
            f"Заявка на ремонт \n{data['client_name']}\nуспешно создана"
        )
        await state.clear()
    else:
        await message.answer("Вы ввели что то не то, введите верное значение!")
