from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from actions_base.actions_users import UserActions

router = Router()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    user = await UserActions.get_user(message.from_user)

    if user.role.name not in ['ADMIN', 'OWNER', 'USER']:
        await message.answer("Обратитесь к Администратору для активации вашего пользователя")
        return

    await message.delete()
    await message.answer("Отменять нечего. Вы вне машины состояний\n\n")


# # Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# # для которых есть отдельные хэндлеры, вне состояний
# @router.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.reply(text='Извините, моя твоя не понимать')