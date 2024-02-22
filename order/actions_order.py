from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from service.service import Service
from states.states import FormOrderChange

order_actions = Router()


@order_actions.message(Command(commands=['change_order']))
async def change_order(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ['admin', 'user']:
        data = await Service.list_order(message.from_user.id)
        answer = "Твои заказы:\n\n"
        for el in data:
            answer += (f'Номер заказа: {el.id}\n'
                       f'Имя клиента: {el.client_name}\n'
                       f'Телефон клиента: {el.client_phone}\n'
                       f'Техника клиента: {el.device}\n'
                       f'Неисправность: {el.mulfunction}\n\n\n\n')

        await message.answer(answer)
        await state.set_state(FormOrderChange.id_order)
        await message.answer(
            f"Введите номер заказа"
        )
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@order_actions.message(FormOrderChange.id_order)
async def change_order_id(message: Message, state: FSMContext):
    await state.update_data(id_order=message.text)
    await state.set_state(FormOrderChange.user_id)
    await message.answer(
        f"Введи новый айди манагера\n\n\n"
    )


@order_actions.message(FormOrderChange.user_id)
async def change_user_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(FormOrderChange.client_name)
    await message.answer(
        f"Введи новое имя клиента"
    )


@order_actions.message(FormOrderChange.client_name)
async def change_client_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(FormOrderChange.client_phone)
    await message.answer(
        f"Введи новый телефон клиента"
    )


@order_actions.message(FormOrderChange.client_phone)
async def change_client_phone(message: Message, state: FSMContext):
    await state.update_data(client_phone=message.text)
    await state.set_state(FormOrderChange.device)
    await message.answer(
        f"Введи вендор и модель техники."
    )


@order_actions.message(FormOrderChange.device)
async def change_device(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrderChange.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@order_actions.message(FormOrderChange.mulfunction)
async def change_mulfunction(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    data = await state.get_data()
    await Service.update_order(data)
    await message.answer(
        f"Заявка на ремонт\n{data['client_name']}\nуспешно изменена"
    )
    await state.clear()