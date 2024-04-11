from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from actions_base.actions_users import UserActions
from models.models import Role


def decorator_permissions(func: Callable) -> Callable:
    async def wrapper(message: Message, state: FSMContext):
        user = await UserActions.get_user(message.from_user)
        if user.role == Role.REGISTERED:
            await message.answer("Обратитсь к администратору за активацией вашего профиля")
        elif user.role not in (Role.ADMIN, Role.OWNER, Role.USER):
            await message.answer("Доступ запрещён")
        else:
            await func(message, state)

    return wrapper


def decorator_permissions_menu(func: Callable) -> Callable:
    async def wrapper(message: Message, dialog_manager: DialogManager):
        user = await UserActions.get_user(message.from_user)
        if not user or user.role == Role.REGISTERED:
            await message.answer("Обратитсь к администратору за активацией вашего профиля")
        else:
            await func(message, dialog_manager)

    return wrapper


def decorator_owner(func: Callable) -> Callable:
    async def wrapper(message: Message, state: FSMContext):
        user = await UserActions.get_user(message.from_user)
        if user.role == Role.OWNER:
            await func(message, state)
        else:
            await message.answer("У вас нет на это прав!")
    return wrapper


def decorator_admin(func: Callable) -> Callable:
    async def wrapper(message: Message, state: FSMContext):
        user = await UserActions.get_user(message.from_user)
        if user.role in [Role.OWNER, Role.ADMIN]:
            await func(message, state)
        else:
            await message.answer("У вас нет на это прав!")

    return wrapper
