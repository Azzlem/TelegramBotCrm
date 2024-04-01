import re

from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from actions_base.actions_users import UserActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.dialog_states import Order
from models.models import Vendor
from permission import is_owner_admin, is_user
from utils import CreateOrderFull


async def vendor_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    vendor_list = []
    for vendor in Vendor:
        vendor_list.append((vendor.name, vendor.name))
    return {'elems': vendor_list}


async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user_from_event = await UserActions.get_user(event_from_user)

    if await is_owner_admin(user_from_event):
        users = await UserActions.get_all_users()
        list_user = []
        for user in users:
            list_user.append((user.fullname, user.id))

        return {'elems': list_user}
    elif await is_user(user_from_event):
        return {'elems': [(user_from_event.fullname, user_from_event.id)]}


async def create_order(callback: CallbackQuery, widget: Button,
                       dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_order)


async def create_customer(callback: CallbackQuery, widget: Button,
                          dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_customer)


async def select_vendor(callback: CallbackQuery, widget: Select,
                        dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['vendor'] = item_id
    await dialog_manager.switch_to(Order.model_item)


async def user_choice(callback: CallbackQuery, widget: Button,
                      dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.user_choice)


async def select_user(callback: CallbackQuery, widget: Select,
                      dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['user'] = item_id

    customer = await CreateOrderFull.create_customer(data=dialog_manager.dialog_data, customer=None)
    order = await CreateOrderFull.create_order(data=dialog_manager.dialog_data, customer=customer)
    item = await CreateOrderFull.create_item(data=dialog_manager.dialog_data, order_id=order.id)

    await callback.message.answer(
        text=f"Заказ {order.id} на технику {item.vendor}-{item.model}\nКлиента {customer.fullname} успешно создан"
    )
    await dialog_manager.start(Order.order_start, mode=StartMode.RESET_STACK)


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


def model_check(text: str):
    if all(ch.isalpha() for ch in text):
        raise ValueError
    return text


def defect_check(text: str):
    if all(ch.isdigit() for ch in text):
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
    await dialog_manager.switch_to(Order.choice_vendor)


async def correct_model_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["model"] = model_check(text)
    await dialog_manager.switch_to(Order.defect)


async def correct_defect_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["defect"] = defect_check(text)
    await dialog_manager.switch_to(Order.user_choice)


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
        text='Вы ввели некорректный телефон. Попробуйте еще раз'
    )


async def incorrect_address_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный адрес. Попробуйте еще раз'
    )


async def incorrect_model_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректную модель. Попробуйте еще раз'
    )


async def incorrect_defect_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный дефект. Попробуйте еще раз'
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
    ),
    Window(
        Const('Выберите Бренд Техники'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='vendor',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_vendor
        ),
            id="elems",
            width=4,
            height=8
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        getter=vendor_getter,
        state=Order.choice_vendor
    ),
    Window(
        Const('Введите модель устройства'),
        TextInput(
            id='model',
            type_factory=model_check,
            on_success=correct_model_handler,
            on_error=incorrect_model_handler,
        ),
        state=Order.model_item

    ),
    Window(
        Const('Опишите неисправность'),
        TextInput(
            id='defect',
            type_factory=defect_check,
            on_success=correct_defect_handler,
            on_error=incorrect_defect_handler,
        ),
        state=Order.defect

    ),
    Window(
        Const('Хотите назначить инженера сразу?'),
        Button(Const('Да'), id='yes', on_click=user_choice),
        Button(Const('Нет'), id='no', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.user_add
    ),
    Window(
        Const('Выберите инженера'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='user',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_user
        ),
            id="elems",
            width=4,
            height=8
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.user_choice,
        getter=user_getter
    )

)