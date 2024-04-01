import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor

from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.dialog_states import Order


async def create_order(callback: CallbackQuery, widget: Button,
                       dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_order)


async def create_customer(callback: CallbackQuery, widget: Button,
                          dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_customer)


def name_check(text: str):
    if all(ch.isdigit() for ch in text):
        raise ValueError
    return re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', text)


def phone_check(text: str):
    if all(ch.isdigit() for ch in text) and len(text) == 7 or len(text) == 11:
        return text
    raise ValueError


def address_check(text: str):
    if all(ch.isdigit() for ch in text) or all(ch.isalpha() for ch in text):
        raise ValueError
    return text


async def correct_name_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["name"] = name_check(text)
    await dialog_manager.switch_to(Order.create_customer_phone)


async def correct_phone_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["phone"] = phone_check(text)
    await dialog_manager.switch_to(Order.create_customer_address)


async def correct_address_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["address"] = address_check(text)
    data = dialog_manager.dialog_data.items()
    print(data)
    # await dialog_manager.switch_to(Order.create_customer_phone)


async def incorrect_name_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректное имя. Попробуйте еще раз'
    )


async def incorrect_phone_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректнsq телефон. Попробуйте еще раз'
    )


async def incorrect_address_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректнsq адрес. Попробуйте еще раз'
    )


order_dialog = Dialog(
    Window(
        Const('Операции с Заказами'),
        Button(Const('Создать заказ'), id='create_order_button', on_click=create_order),
        Button(Const('Найти заказ'), id='find_order_button'),
        Button(Const('Мои заказы'), id='cancel_button'),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),

        state=Order.order_start
    ),
    Window(
        Const('Меню создания заказа'),
        Button(Const('Новый клиент'), id='new_customer_button', on_click=create_customer),
        Button(Const('Выбрать из существующих'), id='choice_customer_button'),
        Button(Const('Назад'), id='back_1', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_order
    ),
    Window(
        Const('Введите Имя или название организации'),
        TextInput(
            id='name_input',
            type_factory=name_check,
            on_success=correct_name_handler,
            on_error=incorrect_name_handler,
        ),
        state=Order.create_customer
    ),
    Window(
        Const('Введите номер телефона'),
        TextInput(
            id='phone_input',
            type_factory=phone_check,
            on_success=correct_phone_handler,
            on_error=incorrect_phone_handler,
        ),
        state=Order.create_customer_phone
    ),
    Window(
        Const('Введите адрес'),
        TextInput(
            id='address_input',
            type_factory=address_check,
            on_success=correct_address_handler,
            on_error=incorrect_address_handler,
        ),
        state=Order.create_customer_address
    )
)
