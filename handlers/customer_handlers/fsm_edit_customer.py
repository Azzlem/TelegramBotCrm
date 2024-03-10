from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from actions_base.actions_customers import CustomerActions
from actions_base.actions_users import UserActions
from keybords.keyboards import keyboard_choice_customer_edit, keyboard_customer_edit
from permission import is_owner_admin
from states.states_customer import FormUpdateCustomer

router = Router()


@router.message(Command(commands="customer_edit"))
async def customer_edit(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_owner_admin(user):
        keyboard = await keyboard_choice_customer_edit()
        await message.answer(
            text="Кого меняем?",
            reply_markup=keyboard
        )
        await state.set_state(FormUpdateCustomer.id)
    else:
        await message.answer("У вас не на это прав")
        await state.clear()


@router.callback_query(StateFilter(FormUpdateCustomer.id))
async def customer_edit_choice_id(callback: CallbackQuery, state: FSMContext):
    await state.update_data(customer_id=int(callback.data))
    await callback.message.delete()
    keyboard = await keyboard_customer_edit()
    await callback.message.answer(
        text="Что будем менять?",
        reply_markup=keyboard
    )
    await state.set_state(FormUpdateCustomer.choice)


@router.callback_query(StateFilter(FormUpdateCustomer.choice), F.data.in_(["fullname"]))
async def customer_edit_fullname(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Напишите новое имя клиента"
    )
    await callback.message.delete()
    await state.set_state(FormUpdateCustomer.fullname)


@router.callback_query(StateFilter(FormUpdateCustomer.choice), F.data.in_(["phone"]))
async def customer_edit_fullname(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Напишите новый телефон клиента"
    )
    await callback.message.delete()
    await state.set_state(FormUpdateCustomer.phone)


@router.callback_query(StateFilter(FormUpdateCustomer.choice), F.data.in_(["adress"]))
async def customer_edit_fullname(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Напишите новый адресс клиента"
    )
    await callback.message.delete()
    await state.set_state(FormUpdateCustomer.address)


@router.callback_query(StateFilter(FormUpdateCustomer.choice), F.data.in_(["email"]))
async def customer_edit_fullname(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Напишите новую почту клиента"
    )
    await callback.message.delete()
    await state.set_state(FormUpdateCustomer.email)


@router.message(StateFilter(FormUpdateCustomer.email), F.text.contains("@"))
async def customer_edit_fullname_final(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await CustomerActions.edit_customer(data)
    await message.answer(
        "Новая почта записано!"
    )


@router.message(StateFilter(FormUpdateCustomer.email))
async def warning_not_email(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на email\n\n'
             'Пожалуйста, введите email клиента\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FormUpdateCustomer.address))
async def customer_edit_fullname_final(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await CustomerActions.edit_customer(data)
    await message.answer(
        "Новый адресс записано!"
    )


@router.message(StateFilter(FormUpdateCustomer.phone), F.text.isdigit())
async def customer_edit_fullname_final(message: Message, state: FSMContext):
    customer = await CustomerActions.get_customer_by_phone(int(message.text))
    if customer:
        await message.answer(text=f'Пользователь с таким телефоном уже зарегистрирован под именем {customer.fullname}')
        await state.clear()
    else:
        await state.update_data(phone=int(message.text))
        data = await state.get_data()
        await CustomerActions.edit_customer(data)
        await message.answer(
            "Новый телефон записано!"
        )


@router.message(StateFilter(FormUpdateCustomer.phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на телефон\n\n'
             'Пожалуйста, введите телефон клиента\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FormUpdateCustomer.fullname))
async def customer_edit_fullname_final(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    data = await state.get_data()
    await CustomerActions.edit_customer(data)
    await message.answer(
        "Новое имя записано!"
    )
