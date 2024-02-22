from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message

from service.service import Service
from states.states import FormChangePermsUser, FormDeleteUser

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


@user_actions.message(Command(commands=["change_perms"]))
async def process_change_perms(message: Message, state: FSMContext) -> None:
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        await state.set_state(FormChangePermsUser.user_id)
        await message.answer(answer)
        await message.answer(
            f"Введи айди манагера\n\n\n"
        )
    else:
        await message.answer("У вас нет на это прав!")


@user_actions.message(FormChangePermsUser.user_id)
async def process_change_perms_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(FormChangePermsUser.status)
    await message.answer(
        f'Введи уровень доступа пользователя.\n'
        f'0 - в доступе отказано\n'
        f'1 - менеджер\n'
        f'2 - админ\n'
    )


@user_actions.message(FormChangePermsUser.status)
async def process_change_perms_status(message: Message, state: FSMContext):
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


@user_actions.message(Command(commands=["del_user"]))
async def del_user(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        await state.set_state(FormDeleteUser.user_id)
        await message.answer(answer)
        await message.answer(
            f"Введи айди манагера\n\n\n"
        )
    else:
        await message.answer("У вас нет на это прав!")


@user_actions.message(FormDeleteUser.user_id)
async def delete_user(message: Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    res = await state.get_data()
    answer = await Service.delete_user(res)
    if answer:
        await message.answer(
            f'Юзер {res["user_id"]} удалён!'
        )
        await state.clear()
    else:
        await message.answer(
            'что то пошло не так'
        )
