from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.check_def import name_check, phone_check, address_check, model_check, defect_check, \
    name_phone_check, price_check
from handlers.dialog_p.correct_handler_order import correct_name_handler, correct_phone_handler, \
    correct_address_handler, correct_model_handler, correct_defect_handler, correct_customer_handler, \
    correct_find_order_handler, correct_component_name_handler, correct_component_price_handler, \
    correct_comment_text_handler
from handlers.dialog_p.dialog_states import Order
from handlers.dialog_p.getters import vendor_getter, user_getter, customers_getter, orders_getter, status_getter
from handlers.dialog_p.utils import format_text
from models.models import Orders
from utils import CreateOrderFull, dowmload_image


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
    await dialog_manager.start(Order.order_start, mode=StartMode.RESET_STACK)


async def select_status(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    if item_id == "exit":
        await dialog_manager.switch_to(Order.actions_choice_orders)
    else:
        dialog_manager.dialog_data['status_order'] = item_id

        await OrdersActions.status_order(
            dialog_manager.dialog_data.get('status_order'),
            int(dialog_manager.dialog_data.get('order_id')),
        )
        await dialog_manager.switch_to(Order.actions_choice_orders)


async def select_customer(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    customer = await CustomerActions.get_customer(int(item_id))
    dialog_manager.dialog_data['customer'] = customer
    await dialog_manager.switch_to(Order.choice_vendor)


async def input_customer_name(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.input_customer_name)


async def find_order(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.find_order)


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


async def send_photo(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_component_photo)


async def send_comment(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_comments)


async def send_status(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.send_status)


async def get_photo_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    bot = dialog_manager.middleware_data.get('bot')
    url = await dowmload_image(message, bot)
    dialog_manager.dialog_data['path_photo'] = url
    await dialog_manager.switch_to(Order.create_component_name)


async def incorrect_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
                            error: ValueError):
    await message.answer(
        text='Вы ввели что-то не то. Попробуйте еще раз'
    )


order_dialog = Dialog(
    Window(
        Const('Операции с Заказами'),
        Button(Const('Создать заказ'), id='create_order_button', on_click=create_order),
        Button(Const('Найти заказ'), id='find_order_button', on_click=find_order),
        Button(Const('Мои заказы'), id='cancel_button'),
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
            type_factory=address_check,
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
            type_factory=defect_check,
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
        Button(Const('Добавить запчасть'), id='send_photo', on_click=send_photo),
        Button(Const('Добавить коментарий'), id='send_comment', on_click=send_comment),
        Button(Const('Изменить статус заказа'), id='send_status', on_click=send_status),
        Button(Const('Назад'), id='back_8', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.actions_choice_orders
    ),
    Window(
        Const('фото чека'),
        MessageInput(
            func=get_photo_handler,
            content_types=ContentType.PHOTO,
        ),
        Button(Const('Назад'), id='back_9', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_component_photo
    ),
    Window(
        Const('Напишите название запчасти'),
        TextInput(
            id='component_name',
            type_factory=name_check,
            on_success=correct_component_name_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Назад'), id='back_10', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_component_name
    ),
    Window(
        Const('Напишите цену'),
        TextInput(
            id='component_name',
            type_factory=price_check,
            on_success=correct_component_price_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Назад'), id='back_11', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_component_price
    ),
    Window(
        Const('Напишите комментарий к заказу'),
        TextInput(
            id='comment_text',
            type_factory=defect_check,
            on_success=correct_comment_text_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Назад'), id='back_12', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_comments
    ),
    Window(
        Const('Выберите статус'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='user',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_status
        ),
            id="elems",
            width=2,
            height=8
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.send_status,
        getter=status_getter
    ),
)
