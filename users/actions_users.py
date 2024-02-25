from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from service import Service
from service_base_actions import ServiceBaseActions
from utils_format import format_data_user_get

user_actions = Router()


@user_actions.message(Command(commands=["reg"]))
async def process_register_command(message: Message):
    if await ServiceBaseActions.get_user(message.from_user):
        await message.answer(f"{message.from_user.username}, вы уже зарегистрированы!")
    else:
        await ServiceBaseActions.add_user(message.from_user)
        await message.answer(
            f'Пользователь {message.from_user.username} успешно создан.\n'
            f'Обратитесь к администратору за активацией.\n'
        )


@user_actions.message(Command(commands=["list_user"]))
async def process_list_user(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await ServiceBaseActions.get_all_users()
        answer_formatting = await format_data_user_get(answer)
        await message.answer(answer_formatting)
    elif await Service.valid_user(message.from_user.id) in ["user"]:
        await message.answer("А тебе это нахуя?")
    else:
        await message.answer("Нехуй тут делать левым людям!!!")
