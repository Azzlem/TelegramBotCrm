from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from service import Service
from states.states import FormDeleteUser
from utils_format import format_data_user_get

delete_user = Router()


@delete_user.message(Command(commands=["del_user"]))
async def delete_user_from_id(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        answer = await format_data_user_get(answer)
        await state.set_state(FormDeleteUser.user_id)
        await message.answer(answer)
        await message.answer(
            f"Введи айди манагера\n\n\n"
        )
    else:
        await message.answer("У вас нет на это прав!")


@delete_user.message(FormDeleteUser.user_id)
async def delete_user_final(message: Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    data = await state.get_data()
    try:
        await Service.delete_user(data)
        await message.answer(
            f'Юзер {data["user_id"]} удалён!'
        )
        await state.clear()
    except:
        await message.answer(
            "Что-то пошло не так!"
        )
    finally:
        await state.clear()
