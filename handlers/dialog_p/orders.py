import re


from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format


from actions_base.actions_components import ComponentActions
from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.dialog_states import Order
from models.models import Vendor, Customers, Orders
from permission import is_owner_admin, is_user
from utils import CreateOrderFull, dowmload_image


async def vendor_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    vendor_list = [(vendor.name, vendor.name) for vendor in Vendor]
    return {'elems': vendor_list}


async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user_from_event = await UserActions.get_user(event_from_user)
    if await is_owner_admin(user_from_event):
        users = await UserActions.get_all_users()
        list_user = [(user.fullname, user.id) for user in users] + [("Не назначать", None)]
    elif await is_user(user_from_event):
        list_user = [(user_from_event.fullname, user_from_event.id)]
    else:
        list_user = []
    return {'elems': list_user}


async def customers_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    customers: list[Customers] = dialog_manager.dialog_data.get('customers_model')
    customer_list = [(customer.fullname, customer.id) for customer in customers]
    return {'elems': customer_list}


async def orders_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    order_list = []
    orders: list[Orders] = dialog_manager.dialog_data.get('orders')
    for order in orders:
        if order.customer is None:
            order_list.append((f'{order.id}', order.id))
        else:
            order_list.append((f'{order.id}-{order.customer.fullname}', order.id))
    return {'elems': order_list}


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


async def select_customer(callback: CallbackQuery, widget: Select,
                          dialog_manager: DialogManager, item_id: str):
    customer = await CustomerActions.get_customer(int(item_id))
    dialog_manager.dialog_data['customer'] = customer
    await dialog_manager.switch_to(Order.choice_vendor)


async def input_customer_name(callback: CallbackQuery, widget: Button,
                              dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.input_customer_name)


async def find_order(callback: CallbackQuery, widget: Button,
                     dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.find_order)


async def actions_orders(callback: CallbackQuery, widget: Button,
                         dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['order_id'] = int(item_id)
    await dialog_manager.switch_to(Order.actions_choice_orders)


async def order_details(callback: CallbackQuery, widget: Button,
                        dialog_manager: DialogManager):
    order: Orders = await OrdersActions.get_all_info_order_users(int(dialog_manager.dialog_data.get('order_id')))
    items = "\n".join(f'{item.vendor.name} - {item.model}' for item in order.items)
    comments = "\n".join(comment.text for comment in order.comments)
    components = "\n".join(f"{component.name} - {component.price}" for component in order.components)
    spending = sum(component.price for component in order.components)
    comments_formatted = "\n".join(f"{i + 1}. {comment}" for i, comment in enumerate(comments.split("\n")))

    await callback.message.answer(
        text=f"""
        <b>Заказ номер:</b> {order.id}

        <b>Клиент:</b> {order.customer.fullname}
        <b>Телефон:</b> {order.customer.phone}
        <b>Адрес:</b> {order.customer.address}

        <b>Инженер:</b> {order.user.fullname if order.user else "Не назначен"}

        <b>Техника:</b>
        {items if order.items else "Без техники"}

...

<b>Коментарии по заказу:</b>

{comments_formatted}

...
...

<b>Запчасти в заказе:</b>
        {'' if components == '' else components}

        ...
        <b>Затраты:</b> {spending}
        <b>Оплачено:</b> {order.price}
        <b>Прибыль:</b> {order.price - spending}
        """,
        parse_mode="HTML"
    )
    # await dialog_manager.switch_to(Order.actions_choice_orders)


async def send_photo(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Order.create_component_photo)


async def get_photo_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    bot = dialog_manager.middleware_data.get('bot')
    url = await dowmload_image(message, bot)
    dialog_manager.dialog_data['path_photo'] = url
    await dialog_manager.switch_to(Order.create_component_name)


def name_check(text: str):
    if all(ch.isdigit() for ch in text):
        raise ValueError
    return re.sub(r'[^a-zA-Zа-яА-Я0-9 ]', '', text)


def name_phone_check(text: str):
    if all(ch.isdigit() for ch in text) and len(text) == 7 or len(text) == 11:
        return text
    else:
        return re.sub(r'[^a-zA-Zа-яА-Я0-9 ]', '', text)


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


def price_check(text: str):
    if all(ch.isdigit() for ch in text):
        return text
    raise ValueError


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


async def correct_customer_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    if all(ch.isdigit() for ch in text):
        customer = [await CustomerActions.get_customer_by_phone(int(text))]
    else:
        customer = await CustomerActions.get_customers_for_fullname(text)
    if customer:
        dialog_manager.dialog_data["customers_model"] = customer
        await dialog_manager.switch_to(Order.choice_customer_button)
    else:
        await message.answer(
            text='Не найден. Попробуйте еще раз'
        )


async def correct_find_order_handler(message: Message,
                                     widget: ManagedTextInput,
                                     dialog_manager: DialogManager,
                                     text: str) -> None:
    if all(ch.isdigit() for ch in text):
        orders = [await OrdersActions.get_order(int(text))]
        if orders[0]:
            dialog_manager.dialog_data["orders"] = orders
            await dialog_manager.switch_to(Order.order_action)
        else:
            customer = await CustomerActions.get_customer_by_phone(int(text))
            if customer:
                orders = await OrdersActions.get_all_orders_to_customer(customer.id)
                dialog_manager.dialog_data["orders"] = orders
                await dialog_manager.switch_to(Order.order_action)
            else:
                await message.answer(
                    text=f"По этому '{text}' номеру клиентов и заказов не найдено.\nПопробуйте ещё раз!")
                await dialog_manager.switch_to(Order.find_order)
    else:
        customer = await CustomerActions.get_customers_for_fullname(text)
        if customer:
            orders = await OrdersActions.get_all_orders_to_customer(customer[0].id)
            dialog_manager.dialog_data["orders"] = orders
            await dialog_manager.switch_to(Order.order_action)
        else:
            await message.answer(text=f"По этому '{text}' имени клиентов и заказов не найдено.\nПопробуйте ещё раз!")
            await dialog_manager.switch_to(Order.find_order)


async def correct_component_name_handler(message: Message,
                                         widget: ManagedTextInput,
                                         dialog_manager: DialogManager,
                                         text: str) -> None:
    dialog_manager.dialog_data["name"] = text
    await dialog_manager.switch_to(Order.create_component_price)


async def correct_component_price_handler(message: Message,
                                          widget: ManagedTextInput,
                                          dialog_manager: DialogManager,
                                          text: str) -> None:
    dialog_manager.dialog_data["price"] = text
    await ComponentActions.create(
        dialog_manager.dialog_data.get('name'),
        dialog_manager.dialog_data.get('path_photo'),
        int(dialog_manager.dialog_data.get('order_id')),
        int(dialog_manager.dialog_data.get('price')),
    )
    await message.answer(
        text="Запчасть успешно добавлена"
    )
    await dialog_manager.switch_to(Order.actions_choice_orders)


async def incorrect_find_order_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели что-то не то. Попробуйте еще раз'
    )


async def incorrect_customer_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректное имя. Попробуйте еще раз'
    )


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
            on_error=incorrect_name_handler,
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
            on_error=incorrect_phone_handler,
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
            on_error=incorrect_address_handler,
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
            on_error=incorrect_model_handler,
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
            on_error=incorrect_defect_handler,
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
            on_error=incorrect_customer_handler,
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
            on_error=incorrect_find_order_handler,
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
        Button(Const('Добавить коментарий'), id='button_start', on_click=dialog_base_def.go_start),
        Button(Const('Закрыть заказ'), id='button_start', on_click=dialog_base_def.go_start),
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
            on_error=incorrect_find_order_handler,
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
            on_error=incorrect_find_order_handler,
        ),
        Button(Const('Назад'), id='back_11', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Order.create_component_price
    ),
)
