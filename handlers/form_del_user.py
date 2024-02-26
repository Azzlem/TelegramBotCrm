from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from UserActionsBase import UserService
from service_base_actions import ServiceBaseActions
from states.states import FormDeleteUser
from utils_format import format_data_user_get

router = Router()


@router.message(Command(commands=["del_user"]))
async def delete_user_from_id(message: Message, state: FSMContext):
    if await UserService.valid_user(message.from_user.id) in ["admin"]:
        answer = await ServiceBaseActions.get_all_users()
        answer = await format_data_user_get(answer)
        await state.set_state(FormDeleteUser.user_id)
        await message.answer(answer)
        await message.answer(
            f"Введи айди манагера\n\n\n"
        )
    else:
        await message.answer("У вас нет на это прав!")


@router.message(FormDeleteUser.user_id)
async def delete_user_final(message: Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    data = await state.get_data()
    try:
        await ServiceBaseActions.delete_user(data)
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
