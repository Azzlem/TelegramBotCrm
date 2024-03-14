from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger
from sqlalchemy.exc import DBAPIError

from actions_base.actions_customers import CustomerActions
from actions_base.actions_items import ItemsActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from formatting.user_formatting import DataObject
from keybords.keyboard_create_order import keyboard_create_order_first, keyboard_create_order_second, \
    keyboard_create_order_third
from keybords.keyboards import keyboard_choise_vendor, keyboard_list_user_for_order
from permission import is_registered, is_owner_admin_user
from states.states_orders import FormCreateOrder

router = Router()


@router.message(Command(commands=["create_order"]))
async def create_order(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_registered(user):
        await message.answer(text="Обратитсь к администратору за активацией вашего профиля")
    elif await is_owner_admin_user(user):
        keyboard = await keyboard_create_order_first()
        await message.answer(text="ВЫБРАТЬ КЛИЕНТА ИЗ СУЩЕСТВУЮЩИХ?", reply_markup=keyboard)
        await state.set_state(FormCreateOrder.create_or_no)


@router.callback_query(StateFilter(FormCreateOrder.create_or_no), F.data == 'y')
async def create_order_callback_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Введите номер телефона или фамилию клиента!")
    await state.set_state(FormCreateOrder.search_customer)


@router.message(StateFilter(FormCreateOrder.search_customer))
async def search_order(message: Message, state: FSMContext):
    keyboard = await keyboard_create_order_second(message.text)
    keyboard_first = await keyboard_create_order_first()
    if not keyboard:
        await message.answer(text="Такого клиента не существует")
        await message.answer(text="ВЫБРАТЬ КЛИЕНТА ИЗ СУЩЕСТВУЮЩИХ?", reply_markup=keyboard_first)
        await state.set_state(FormCreateOrder.create_or_no)
    else:
        await message.answer(text="ВЫБЕРИТЕ КЛИЕНТА", reply_markup=keyboard)
        await state.set_state(FormCreateOrder.choice_customer)


@router.callback_query(StateFilter(FormCreateOrder.choice_customer))
async def search_order_customer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(customer_id=int(callback.data))
    await callback.message.delete()
    keyboard = await keyboard_choise_vendor()
    await callback.message.answer(
        text="Добавьте технику к заказу",
        reply_markup=keyboard
    )
    await state.set_state(FormCreateOrder.vendor_choice)


@router.callback_query(StateFilter(FormCreateOrder.vendor_choice))
async def choice_customer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(vendor=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        'Введите модель техники'
    )
    await state.set_state(FormCreateOrder.model)


@router.message(StateFilter(FormCreateOrder.model))
async def add_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer(
        "Напишите неисправность"
    )
    await state.set_state(FormCreateOrder.defect)


@router.message(StateFilter(FormCreateOrder.defect))
async def add_defect(message: Message, state: FSMContext):
    await state.update_data(defect=message.text)
    keyboard = await keyboard_create_order_third()
    await message.answer(
        text="Хотите назначить инженера сразу?",
        reply_markup=keyboard
    )
    await state.set_state(FormCreateOrder.user_choice)


@router.callback_query(StateFilter(FormCreateOrder.user_choice), F.data == 'yes')
async def yes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    keyboard = await keyboard_list_user_for_order(callback.from_user)
    await callback.message.answer(
        text="Выберите инженера",
        reply_markup=keyboard
    )
    await state.set_state(FormCreateOrder.user_id)


@router.callback_query(StateFilter(FormCreateOrder.user_id))
async def user_id_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(user_id=callback.data)
    await callback.message.delete()
    data = await state.get_data()
    data = DataObject(data=data)
    try:
        if data.customer_id is None:
            customer = await CustomerActions.add_customer_in_orger(data.fullname, data.phone, data.address)
        else:
            customer = await CustomerActions.get_customer(data.customer_id)
        user = await UserActions.get_user_from_id(data)
        order = await OrdersActions.create_orders(customer.id, data.user_id)
        item = await ItemsActions.add_item_to_order(data.vendor, data.model, data.defect, order.id)
        await callback.message.answer(
            text=f"{customer.fullname} - {order.id} - {item.id}"
        )
        await bot.send_message(user.telegram_id, text=f"Вы {user.username}\n"
                                                      f"Назначены на заказ №{order.id}\n"
                                                      f"Имя клиента: {customer.fullname}\n"
                                                      f"Адрес:  {customer.address}\n"
                                                      f"Техника: {item.vendor} - {item.model}\n"
                                                      f"Неисправность: {item.defect}\n")
        await state.clear()

    except DBAPIError:
        logger.add("logs/file_{time}.json", rotation="weekly")
        logger.exception("What?!")


@router.callback_query(StateFilter(FormCreateOrder.create_or_no), F.data == 'n')
async def create_order_callback_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Ну и чего приходил?")
    await state.clear()


@router.callback_query(StateFilter(FormCreateOrder.create_or_no), F.data == 'c')
async def create_order_callback_create(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Введите Имя и Фамилию клиента. Ну или просто имя. Ну или название организации.')
    await state.set_state(FormCreateOrder.fullname)


@router.message(StateFilter(FormCreateOrder.fullname))
async def add_customer_fullname(message: Message, state: FSMContext):
    row = []
    for el in message.text.split():
        row.append(el.isalpha())
    if not False in row:
        await state.update_data(fullname=message.text)
        await message.answer(
            "Введите номер телефона клиента"
        )
        await state.set_state(FormCreateOrder.phone)
    else:
        await message.answer("Это не похоже на имя и фамилию. Введи то что просят!")


@router.message(StateFilter(FormCreateOrder.phone), F.text.isdigit())
async def add_customer_phone(message: Message, state: FSMContext):
    customer = await CustomerActions.get_customer_by_phone(int(message.text))
    if customer:
        await message.answer(text=f'Пользователь с таким телефоном уже зарегистрирован под именем {customer.fullname}')
        await state.set_state(FormCreateOrder.phone)
    else:
        await state.update_data(phone=int(message.text))
        await message.answer(
            "Введите адрес клиента"
        )
        await state.set_state(FormCreateOrder.address)


@router.message(StateFilter(FormCreateOrder.phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на телефон\n\n'
             'Пожалуйста, введите телефон клиента\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


@router.message(StateFilter(FormCreateOrder.address))
async def warning_not_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    keyboard = await keyboard_choise_vendor()
    await message.answer(
        text="Добавьте технику к заказу",
        reply_markup=keyboard
    )
    await state.set_state(FormCreateOrder.vendor_choice)
