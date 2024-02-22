from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from service.service import Service
from states.states import FormOrder

router_order_create = Router()


@router_order_create.message(Command('order'))
async def command_order(message: Message, state: FSMContext) -> None:
    await state.set_state(FormOrder.user_id)
    await message.answer(
        "Введи айди манагера",
    )


@router_order_create.message(FormOrder.user_id)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(FormOrder.client_name)
    await message.answer(
        f"Введи имя клиента"
    )


@router_order_create.message(FormOrder.client_name)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(FormOrder.client_phone)
    await message.answer(
        f"Введи телефон клиента"
    )


@router_order_create.message(FormOrder.client_phone)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(client_phone=message.text)
    await state.set_state(FormOrder.device)
    await message.answer(
        f"Введи вендор и модель техники."
    )


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
    data = await state.get_data()
    await Service.add_order(data)
    await message.answer(
        f"Заявка на ремонт \n{data['client_name']}\nуспешно создана"
    )
    await state.clear()


@router_order_create.message(Command(commands=["list_orders"]))
async def process_list_orders(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
        data = await Service.list_order(message.from_user.id)
        answer = "Заказы общие:\n\n"
        for el in data:
            answer += (f'Номер заказа: {el.id}\n'
                       f'Имя клиента: {el.client_name}\n'
                       f'Телефон клиента: {el.client_phone}\n'
                       f'Техника клиента: {el.device}\n'
                       f'Неисправность: {el.mulfunction}\n\n\n\n')

        await message.answer(answer)
    else:
        await message.answer("И хули мы тут шаримся?")
