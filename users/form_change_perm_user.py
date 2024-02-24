from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from service import Service
from states.states import FormChangePermsUser
from utils_format import format_data_user_get

change_perm_user = Router()


@change_perm_user.message(Command(commands=["change_perms"]))
async def process_change_perms(message: Message, state: FSMContext) -> None:
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        answer = await format_data_user_get(answer)
        await state.set_state(FormChangePermsUser.user_id)
        await message.answer(answer)
        await message.answer(
            f"Введи айди манагера\n\n\n"
        )
    else:
        await message.answer("У вас нет на это прав!")


@change_perm_user.message(FormChangePermsUser.user_id)
async def process_change_perms_id(message: Message, state: FSMContext) -> None:
    await state.update_data(user_id=message.text)
    await state.set_state(FormChangePermsUser.status)
    await message.answer(
        f'Введи уровень доступа пользователя.\n'
        f'0 - в доступе отказано\n'
        f'1 - менеджер\n'
        f'2 - админ\n'
    )


@change_perm_user.message(FormChangePermsUser.status)
async def process_change_perms_status(message: Message, state: FSMContext) -> None:
    await state.update_data(status=message.text)
    data = await state.get_data()
    answer_service = await Service.change_perms_user(data)
    if answer_service:
        await message.answer(
            f'Права пользователя {data["user_id"]}\n'
            f'изменены на {data["status"]}\n'
        )
        await state.clear()
    else:
        await message.answer(
            "не вышло"
        )
        await state.clear()

