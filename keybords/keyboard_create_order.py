from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from actions_base.actions_customers import CustomerActions
from loguru import logger
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from models.models import Role, Vendor
from permission import is_owner_admin


async def keyboard_create_order_first() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text="ДА", callback_data='y'),
                                           InlineKeyboardButton(text="НЕТ, СОЗДАТЬ НОВОГО", callback_data='c'),
                                           InlineKeyboardButton(text="ОТМЕНА", callback_data='n')]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


async def keyboard_create_order_second(data) -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if data.isalpha():
        customers = await CustomerActions.get_customers_for_fullname(data)
        if not customers:
            return False
        elif isinstance(customers, list):
            for customer in customers:
                buttons.append(InlineKeyboardButton(
                    text=f"{customer.fullname}",
                    callback_data=f"{customer.id}"
                ))
        else:
            buttons.append(InlineKeyboardButton(
                text=f"{customers.fullname}",
                callback_data=f"{customers.id}"
            ))
    elif data.isdigit():
        customers = await CustomerActions.get_customer_by_phone(int(data))
        if not customers:
            return False
        elif isinstance(customers, list):
            for customer in customers:
                buttons.append(InlineKeyboardButton(
                    text=f"{customer.fullname}",
                    callback_data=f"{customer.id}"
                ))
        else:
            buttons.append(InlineKeyboardButton(
                text=f"{customers.fullname}",
                callback_data=f"{customers.id}"
            ))
    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


async def keyboard_create_order_third() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text="ДА", callback_data='yes'),
                                           InlineKeyboardButton(text="НЕТ", callback_data='no'),
                                           InlineKeyboardButton(text="ОТМЕНА Заказа я еблан", callback_data='eblan')]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
