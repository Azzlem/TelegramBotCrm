from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from actions_base.actions_customers import CustomerActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.dialog_base_def import go_start
from handlers.dialog_p.dialog_states import Customer
from models.models import Customers


async def customer_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    customers = dialog_manager.dialog_data.get('customers')
    print(customers)
    return {'customer': customers.fullname}


async def go_find_client(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Customer.find)


async def go_choice_client(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Customer.list_customer)


async def well_done(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    customer: Customers = dialog_manager.dialog_data.get('customers')
    await callback.message.answer(text=f"КЛИЕНТ\n"
                                       f"Имя: {customer.fullname}\n"
                                       f"Адрес: {customer.address}\n"
                                       f"Телефон: {customer.phone}\n")
    await dialog_manager.reset_stack()


def phone_fio_check(text: str) -> int | str:
    if all(ch.isdigit() for ch in text) and (len(text) == 11 or len(text) == 7):
        return int(text)
    elif all(ch.isalpha() for ch in text):
        return text.lower()
    raise ValueError


# Хэндлер, который сработает, если пользователь ввел корректный возраст
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


clients_dialog = Dialog(
    Window(
        Const('Клиенты'),
        Row(
            Button(Const('Найти клиента'), id='button_find_client', on_click=go_find_client),
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=go_start),
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
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=go_start),
        state=Customer.find
    ),
    Window(
        Const('Список Клинтов по вашему запросу'),
        TextInput(
            id='choice_customer',

        ),
        Button(Format('{customer}'), id='customer', on_click=well_done),
        Button(Const('Назад'), id='back_2', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=go_start),
        getter=customer_getter,
        state=Customer.list_customer
    ),
)
