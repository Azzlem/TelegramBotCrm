from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from actions_base.actions_customers import CustomerActions
from actions_base.actions_users import UserActions
from permission import is_owner_admin_user
from states.states_customer import FormAddCustomer

router = Router()


@router.message(Command(commands=["customer_add"]))
async def add_customer(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_owner_admin_user(user):
        await message.answer('Введите Имя и Фамилию клиента. Ну или просто имя.')
        await state.set_state(FormAddCustomer.fullname)
    else:
        await message.answer(text="У вас нет прав!")
        await state.clear()


@router.message(StateFilter(FormAddCustomer.fullname))
async def add_customer_fullname(message: Message, state: FSMContext):
    row = []
    for el in message.text.split():
        row.append(el.isalpha())
    if not False in row:
        await state.update_data(fullname=message.text)
        await message.answer(
            "Введите номер телефона клиента"
        )
        await state.set_state(FormAddCustomer.phone)
    else:
        await message.answer("Это не похоже на имя и фамилию. Введи то что просят!")


@router.message(StateFilter(FormAddCustomer.phone), F.text.isdigit())
async def add_customer_phone(message: Message, state: FSMContext):
    await state.update_data(phone=int(message.text))
    await message.answer(
        "Введите адрес клиента"
    )
    await state.set_state(FormAddCustomer.address)


@router.message(StateFilter(FormAddCustomer.phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на телефон\n\n'
             'Пожалуйста, введите телефон клиента\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FormAddCustomer.address))
async def warning_not_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    customer = await CustomerActions.add_customer(data)
    await message.answer(
        text=f"Клиент {customer.fullname} создан!"
    )
