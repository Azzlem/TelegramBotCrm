from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from actions_base.actions_users import UserActions
from formatting.user_formatting import UserFormatter
from service_base_actions import ServiceBaseActions
from utils_format import format_data_user_get
router = Router()


@router.message(Command(commands=["reg"]))
async def process_register_command(message: Message):
    if await UserActions.get_user(message.from_user):
        await message.answer(f"{message.from_user.username}, вы уже зарегистрированы!")
    else:
        user = await UserActions.add_user(message.from_user)
        await message.answer(
            f'Пользователь {user.username} успешно создан.\n'
            f'Обратитесь к администратору за активацией.\n'
        )


@router.message(Command(commands=["list_user"]))
async def process_list_user(message: Message):
    user = await UserActions.get_user(message.from_user)
    if user.role.name in ["REGISTERED", "USER"]:
        await message.answer(
            text="У вас нет прав!"
        )
    elif user.role.name in ["ADMIN", "OWNER"]:
        users = await UserActions.get_all_users()
        users = await UserFormatter.convert_to_base_list(users)
        await message.answer(
            text=users
        )
