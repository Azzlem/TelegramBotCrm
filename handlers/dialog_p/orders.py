from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format
from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from dataclass import DataClass
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.check_def import (name_check, phone_check, must_be_num_and_str_check, model_check,
                                         not_only_num_check, name_phone_check)
from handlers.dialog_p.correct_handler_order import correct_name_handler, correct_phone_handler, \
    correct_address_handler, correct_model_handler, correct_defect_handler, correct_customer_handler, \
    correct_find_order_handler
from handlers.dialog_p.dialog_states import Order, Comment, Component, StatusOrder
from handlers.dialog_p.icorrect_handlers import incorrect_handler
from handlers.dialog_p.getters import vendor_getter, user_getter, customers_getter, orders_getter, my_order_getter
from handlers.dialog_p.utils import format_text
from models.models import Orders, Users
from utils import CreateOrderFull


async def start_add_comment(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(Comment.get_comments, data={"order_id": dialog_manager.dialog_data.get('order_id')})


async def create_order(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_order)


async def create_customer(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_customer)


async def select_vendor(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['vendor'] = item_id
    await dialog_manager.switch_to(Order.model_item)


async def user_choice(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.user_choice)


async def select_user(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['user'] = item_id
    dialog_manager.dialog_data['id'] = item_id
    telegram_id = DataClass(dialog_manager.dialog_data)
    user_to_appointed: Users = await UserActions.get_user_from_id(telegram_id)
    if not dialog_manager.dialog_data.get('customer'):
        customer = await CreateOrderFull.create_customer(data=dialog_manager.dialog_data, customer=None)
        order = await CreateOrderFull.create_order(data=dialog_manager.dialog_data, customer=customer)
        item = await CreateOrderFull.create_item(data=dialog_manager.dialog_data, order_id=order.id)
    else:
        customer = dialog_manager.dialog_data['customer']
        order = await CreateOrderFull.create_order(data=dialog_manager.dialog_data, customer=customer)
        item = await CreateOrderFull.create_item(data=dialog_manager.dialog_data, order_id=order.id)

    await callback.message.answer(
        text=f"Заказ {order.id} на технику {item.vendor}-{item.model}\nКлиента {customer.fullname} успешно создан"
    )
    bot = dialog_manager.middleware_data.get('bot')
    await bot.send_message(
        chat_id=user_to_appointed.telegram_id,
        text=f"Заказ {order.id} на технику {item.vendor}-{item.model}\nКлиента {customer.fullname} вам назначен.\n"
             f"Зайдите в ваши заказы и поменяйте статус на принят у вас 20 минут потом полетит штраф."
    )
    await dialog_manager.start(Order.order_start, mode=StartMode.RESET_STACK)


async def select_status_start(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(StatusOrder.get_status, data={"order_id": dialog_manager.dialog_data.get('order_id')})


async def select_customer(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    customer = await CustomerActions.get_customer(int(item_id))
    dialog_manager.dialog_data['customer'] = customer
    await dialog_manager.switch_to(Order.choice_vendor)


async def select_my_order(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['order_id'] = int(item_id)
    await dialog_manager.switch_to(Order.my_order_actions)


async def input_customer_name(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.input_customer_name)


async def find_order(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.find_order)


async def get_my_orders(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.get_my_orders)


async def actions_orders(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['order_id'] = int(item_id)
    await dialog_manager.switch_to(Order.actions_choice_orders)


async def order_details(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    order: Orders = await OrdersActions.get_all_info_order_users(int(dialog_manager.dialog_data.get('order_id')))
    text = await format_text(order)
    await callback.message.answer(
        text=text,
        parse_mode="HTML"
    )


async def get_photo_receipt(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.start(
        Component.get_photo_receipt,
        data={"order_id": dialog_manager.dialog_data.get('order_id')}
    )


order_dialog = Dialog(
    Window(
        Const('Операции с Заказами'),
        Button(Const('Создать заказ'), id='create_order_button', on_click=create_order),
        Button(Const('Найти заказ'), id='find_order_button', on_click=find_order),
        Button(Const('Мои заказы'), id='get_my_orders', on_click=get_my_orders),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),

        state=Order.order_start
    ),
    Window(
        Const('Меню создания заказа'),
        Button(Const('Новый клиент'), id='new_customer_button', on_click=create_customer),
        Button(Const('Выбрать из существующих'), id='input_customer_name', on_click=input_customer_name),
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
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_customer
    ),
    Window(
        Const('Введите номер телефона'),
        TextInput(
            id='phone_input',
            type_factory=phone_check,
            on_success=correct_phone_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_customer_phone
    ),
    Window(
        Const('Введите адрес'),
        TextInput(
            id='address_input',
            type_factory=must_be_num_and_str_check,
            on_success=correct_address_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
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
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.model_item

    ),
    Window(
        Const('Опишите неисправность'),
        TextInput(
            id='defect',
            type_factory=not_only_num_check,
            on_success=correct_defect_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
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
    ),
    Window(
        Const('Напишите название организации, Фамилию или номер телефона клиента'),
        TextInput(
            id='customer_choice_text',
            type_factory=name_phone_check,
            on_success=correct_customer_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.input_customer_name
    ),
    Window(
        Const('Выберите клиента'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='user',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_customer
        ),
            id="elems",
            width=3,
            height=8
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.choice_customer_button,
        getter=customers_getter
    ),
    Window(
        Const('Напишите название организации, Фамилию,  номер телефона клиента'),
        TextInput(
            id='customer_choice_text',
            type_factory=name_phone_check,
            on_success=correct_find_order_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.find_order
    ),
    Window(
        Const('Выберите заказ'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='user',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=actions_orders
        ),
            id="elems",
            width=3,
            height=8
        ),
        Button(Const('Назад'), id='back_7', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.order_action,
        getter=orders_getter
    ),
    Window(
        Const('Выбранный вами заказ'),
        Button(Const('Подробности'), id='button_detail_order', on_click=order_details),
        Button(Const('Добавить запчасть'), id='send_photo', on_click=get_photo_receipt),
        Button(Const('Добавить коментарий'), id='send_comment', on_click=start_add_comment),
        Button(Const('Изменить статус заказа'), id='send_status', on_click=select_status_start),
        Button(Const('Назад'), id='back_8', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.actions_choice_orders
    ),
    Window(
        Const('Выберите заказ]'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='my_order',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_my_order
        ),
            id="elems",
            width=1,
            height=6
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.get_my_orders,
        getter=my_order_getter
    ),
    Window(
        Const('Что будем делать?'),
        Button(Const('Добавить запчасть'), id='add_component', on_click=get_photo_receipt),
        Button(Const('Добавить Комментарий'), id='my_order_add_comment', on_click=start_add_comment),
        Button(Const('Изменить статус'), id='change_status', on_click=select_status_start),
        Button(Const('Внести деньги'), id='button_start', on_click=dialog_base_def.go_start),
        Button(Const('Вернуться в главное меню'), id='exit_button', on_click=dialog_base_def.go_start),
        state=Order.my_order_actions,
    ),
)
