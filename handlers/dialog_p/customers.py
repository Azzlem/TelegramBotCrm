from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Row, Button, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from handlers.dialog_p import dialog_base_def

from handlers.dialog_p.dialog_states import Customer
from models.models import Customers


# Получение списка клиентов для кнопок выбора
async def customer_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    customers: Customers | list = dialog_manager.dialog_data.get('customers')
    if customers is None:
        return {'elems': [("нет такого клиента", "0")]}
    elif isinstance(customers, list):
        elems: list = []
        for customer in customers:
            elems.append((customer.fullname, customer.id))
        return {'elems': elems}
    else:
        return {'elems': [(customers.fullname, customers.id)]}


async def customer_getter_orders(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    customer_id: str = dialog_manager.dialog_data.get('customer_id')
    orders = await OrdersActions.get_all_orders_to_customer(int(customer_id))
    orders_list: list = []
    if not orders:
        return {'elems': [("нет заказов", "0")]}
    else:
        for order in orders:
            orders_list.append((f'{order.id}-{order.status.name}', order.id))
        orders_list = sorted(orders_list, key=lambda x: x[1], reverse=True)
        return {'elems': orders_list}


async def go_find_client(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Customer.find)


async def go_choice_client(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Customer.list_customer)


async def customer_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    if item_id == "0":
        await callback.message.delete()
        await callback.message.answer("Написано же нет клиентов")
        await dialog_manager.switch_to(Customer.find)
    else:
        customer: Customers = await CustomerActions.get_customer(int(item_id))
        dialog_manager.dialog_data['customer_id'] = item_id
        await callback.message.answer(text=f"КЛИЕНТ\n"
                                           f"Имя: {customer.fullname}\n"
                                           f"Адрес: {customer.address}\n"
                                           f"Телефон: {customer.phone}\n")
        await dialog_manager.switch_to(Customer.list_customer_choice)


# Обработчик выбора заказа
async def customer_selection_order(callback: CallbackQuery, widget: Select,
                                   dialog_manager: DialogManager, item_id: str):
    if item_id == "0":
        await callback.message.delete()
        await callback.message.answer("Написано же нет клиентов")
        await dialog_manager.switch_to(Customer.find)
    else:
        order = await OrdersActions.get_all_info_order_users(int(item_id))
        price_components = 0
        if len(order.components) > 0:
            for component in order.components:
                price_components += int(component.price)
        else:
            pass
        await callback.message.answer(text=f'Заказ номер: {order.id}\n'
                                           f'Клиент: {order.customer.fullname}\n'
                                           f'Адресс: {order.customer.address}\n'
                                           f'Статус: {order.status.name}\n'
                                           f'Затраты: {price_components}\n'
                                           f'Оплачено: {order.price}\n'
                                           f'Прибыль: {order.price - price_components}\n'
                                           f'Инженер: {order.user.fullname}')


def phone_fio_check(text: str) -> int | str:
    if all(ch.isdigit() for ch in text) and (len(text) == 11 or len(text) == 7):
        return int(text)
    elif all(ch.isalpha() for ch in text):
        return text.lower()
    raise ValueError


# Хэндлер, который сработает, если пользователь ввел корректный телефон
async def correct_phone_fio_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    if isinstance(text, int):
        customer: Customers = await CustomerActions.get_customer_by_phone(text)
        dialog_manager.dialog_data['customers'] = customer
        await message.answer(text=f'ФИО клиента: {customer.fullname}')
    elif isinstance(text, str):
        customers: list = await CustomerActions.get_customers_for_fullname(text)
        if len(customers) == 0:
            await message.answer(text="Не найдено")
        else:
            dialog_manager.dialog_data['customers'] = customers
            await message.answer(text=f'Телефон клиента: {customers[0].phone}')
    dialog_manager.dialog_data['phone_client'] = text
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного возраста
async def error_phone_fio_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str):
    await message.answer(
        text='Вы ввели некорректный номер. Попробуйте еще раз'
    )


async def list_order(callback: CallbackQuery, widget: Button,
                     dialog_manager: DialogManager):
    await callback.message.delete()
    await dialog_manager.switch_to(Customer.list_order)


customer_dialog = Dialog(
    Window(
        Const('Клиенты'),
        Row(
            Button(Const('Найти клиента'), id='button_find_client', on_click=go_find_client),
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Customer.customer
    ),
    Window(
        Const('Введите телефон или фамилию клиента\n'),
        TextInput(
            id='phone_fio_input',
            type_factory=phone_fio_check,
            on_success=correct_phone_fio_handler,
            on_error=error_phone_fio_handler,
        ),
        Button(Const('Назад'), id='back_1', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Customer.find
    ),
    Window(
        Const('Список Клинтов по вашему запросу'),
        Select(
            Format('{item[0]}'),
            id='customer',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=customer_selection,
        ),
        Button(Const('Назад'), id='back_2', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        getter=customer_getter,
        state=Customer.list_customer
    ),
    Window(
        Const("Подробная информация о клиенте"),
        Button(Const("Список заказов"), id='list_order', on_click=list_order),
        Button(Const('Назад'), id='back_3', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Customer.list_customer_choice
    ),
    Window(
        Const("Список заказов"),
        ScrollingGroup(
            Select(Format('{item[0]}'),
                   id='customer',
                   item_id_getter=lambda x: x[1],
                   items='elems',
                   on_click=customer_selection_order,
                   ),
            id="elems",
            width=3,
            height=3
        ),

        Button(Const('Назад'), id='back_3', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Customer.list_order,
        getter=customer_getter_orders
    )
)
