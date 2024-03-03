from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from service_base_actions import ServiceBaseActions

router = Router()


@router.message(Command(commands='help'))
async def process_help(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
        await message.answer(
            f"Это бот база\n"
        )
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
        await message.answer(
            text='Отменять нечего. Вы вне машины состояний\n\n'
        )
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


