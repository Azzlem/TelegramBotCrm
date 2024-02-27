from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from OrderActionsBase import OrderService
from keybords.keyboards import keyboard_create_orders_user, keyboard_create_orders_users, keyboard_change_order
from service_base_actions import ServiceBaseActions
from states.states import FormOrderChange

router = Router()


@router.message(Command(commands=['change_order']))
async def change_order(message: Message, state: FSMContext):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ['admin', 'user']:
        keyboard = await keyboard_change_order(message.from_user)
        await message.answer(
            text="Введите номер заказа",
            reply_markup=keyboard
        )
        await state.set_state(FormOrderChange.order_id)
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@router.callback_query(StateFilter(FormOrderChange.order_id),
                       F.data.in_([str(el) for el in range(1500)]))
async def change_order_callback_query(callback: CallbackQuery, state: FSMContext):
    await state.update_data(order_id=int(callback.data))
    await callback.message.delete()
    if await ServiceBaseActions.valid_user(callback.from_user.id) in ["admin"]:
        keyboard = await keyboard_create_orders_users()
    else:
        keyboard = await keyboard_create_orders_user(callback.from_user.id)

    await callback.message.answer(
        text='Выберите инженера!',
        reply_markup=keyboard
    )
    await state.set_state(FormOrderChange.user_id)


@router.callback_query(StateFilter(FormOrderChange.user_id),
                       F.data.in_([str(el) for el in range(15)]))
async def change_order_callback_user_query(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=int(callback.data))
    await callback.message.delete()

    await callback.message.answer(
        f"Введи новое имя клиента"
    )
    await state.set_state(FormOrderChange.client_name)


@router.message(FormOrderChange.client_name)
async def change_client_name(message: Message, state: FSMContext):
    row = []
    for el in message.text.split():
        row.append(el.isalpha())
    if not False in row:
        await state.update_data(client_name=message.text)
        await state.set_state(FormOrderChange.client_phone)
        await message.answer(
            f"Введи телефон клиента"
        )
    else:
        await message.answer("Это не похоже на имя, введи имя не еби мозги!")


@router.message(FormOrderChange.client_phone)
async def change_client_phone(message: Message, state: FSMContext):
    if len(message.text) == 11 or len(message.text) == 7:
        await state.update_data(client_phone=message.text)
        await state.set_state(FormOrderChange.device)
        await message.answer(
            f"Введи вендор и модель техники."
        )
    else:
        await message.answer("Ты правда думаешь что если на отъебись заполнять форму то ты станешь миллионером?")


@router.message(FormOrderChange.device)
async def change_device(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(FormOrderChange.mulfunction)
    await message.answer(
        f"Введи неисправность техники."
    )


@router.message(FormOrderChange.mulfunction)
async def change_mulfunction(message: Message, state: FSMContext):
    await state.update_data(mulfunction=message.text)
    data = await state.get_data()
    await OrderService.update_order(data)
    await message.answer(
        f"Заявка на ремонт\n{data['client_name']}\nуспешно изменена"
    )
    await state.clear()
