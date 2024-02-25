from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service import Service
from service_base_actions import ServiceBaseActions


async def keyboard_create_order_user() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    users = await ServiceBaseActions.get_all_users()
    for user in users:
        buttons.append(InlineKeyboardButton(
            text=f"{user.name}",
            callback_data=f"{user.id}"
        ))

    kb_builder.row(*buttons, width=8)

    return kb_builder.as_markup()


async def keyboard_change_order_orders() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    orders = await Service.get_all_orders_scalar()
    for order in orders:
        buttons.append(InlineKeyboardButton(
            text=f"{order.id} - {order.device} - {order.client_name}",
            callback_data=f"{order.id}"
        ))

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()
