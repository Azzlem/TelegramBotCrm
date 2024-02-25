from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service import Service
from service_base_actions import ServiceBaseActions


async def keyboard_create_orders_user(tg_user_id) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    user = await ServiceBaseActions.get_user(tg_user_id)

    buttons.append(InlineKeyboardButton(
        text=f"{user.name}",
        callback_data=f"{user.id}"
    ))

    kb_builder.row(*buttons, width=8)

    return kb_builder.as_markup()


async def keyboard_create_orders_users() -> InlineKeyboardMarkup:
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


async def keyboard_change_order_orders(data) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    orders = await Service.get_all_orders_user(data)
    print(orders)
    for order in orders:
        print(order.id)
        buttons.append(InlineKeyboardButton(
            text=f"{order.id} - {order.device} - {order.client_name}",
            callback_data=f"{order.id}"
        ))

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()


async def keyboard_change_orders_orders() -> InlineKeyboardMarkup:
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
