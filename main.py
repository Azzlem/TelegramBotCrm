from aiogram import Bot, Dispatcher

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from service import Service
from settings import settings

TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
storage = MemoryStorage()


class Form(StatesGroup):
    user_id = State()
    client_name = State()
    client_phone = State()
    device = State()
    mulfunction = State()


@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /order'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /order'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@dp.message(Command('order'))
async def command_order(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_id)
    await message.answer(
        "Введи айди манагера",
    )


@dp.message(Form.user_id)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await state.set_state(Form.client_name)
    await message.answer(
        f"Введи имя клиента"
    )


@dp.message(Form.client_name)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(Form.client_phone)
    await message.answer(
        f"Введи телефон клиента"
    )


@dp.message(Form.client_phone)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(client_phone=message.text)
    await state.set_state(Form.device)
    await message.answer(
        f"Введи вендор и модель техники."
    )


@dp.message(Form.device)
async def command_name(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(Form.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@dp.message(Form.mulfunction)
async def command_age(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    data = await state.get_data()
    await Service.add_order(data)
    await message.answer(
        f"Заявка на ремонт \n{data['client_name']}\nуспешно создана"
    )
    await state.clear()


@dp.message(Command(commands=["registr"]))
async def process_register_command(message: Message):
    if await Service.get_user(message.from_user.id):
        await message.answer(f"{message.from_user.username}, вы уже зарегистрированы!")
    else:
        answer = await Service.add_user(message.from_user.username, message.from_user.id)
        await message.answer(f"{answer} - вы успешно зарегистрированы")


@dp.message(Command(commands=["list_orders"]))
async def process_list_orders(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
        data = await Service.list_order(message.from_user.id)
        answer = "Заказы общие:\n\n"
        for el in data:
            answer += (f'Номер заказа: {el.id}\n'
                       f'Имя клиента: {el.client_name}\n'
                       f'Телефон клиента: {el.client_phone}\n'
                       f'Техника клиента: {el.device}\n'
                       f'Неисправность: {el.mulfunction}\n\n\n\n')

        await message.answer(answer)
    else:
        await message.answer("И хули мы тут шаримся?")


@dp.message(Command(commands=["list_user"]))
async def process_list_user(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
        answer = await Service.get_all_users()
        await message.answer(answer)
    elif await Service.valid_user(message.from_user.id) in ["user"]:
        await message.answer("А тебе это нахуя?")
    else:
        await message.answer("Нехуй тут делать левым людям!!!")


if __name__ == '__main__':
    dp.run_polling(bot)
