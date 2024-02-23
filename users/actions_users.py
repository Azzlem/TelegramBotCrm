from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from service import Service


user_actions = Router()


@user_actions.message(Command(commands=["registr"]))
async def process_register_command(message: Message):
    if await Service.get_user(message.from_user.id):
        await message.answer(f"{message.from_user.username}, вы уже зарегистрированы!")
    else:
        answer = await Service.add_user(message.from_user.username, message.from_user.id)
        await message.answer(f"{answer} - вы успешно зарегистрированы")


@user_actions.message(Command(commands=["list_user"]))
async def process_list_user(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        await message.answer(answer)
    elif await Service.valid_user(message.from_user.id) in ["user"]:
        await message.answer("А тебе это нахуя?")
    else:
        await message.answer("Нехуй тут делать левым людям!!!")
