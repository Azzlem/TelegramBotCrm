from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from actions_base.actions_order import OrdersActions
from actions_base.actions_users import UserActions
from models.models import Role, Vendor


async def keyboard_list_user() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    users = await UserActions.get_all_users()
    for user in users:
        buttons.append(InlineKeyboardButton(
            text=f"{user.id} - {user.fullname}",
            callback_data=f"{user.id}"
        ))
    kb_builder.row(*buttons, width=5)

    return kb_builder.as_markup()


async def keyboard_list_orders() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    roles = Role
    for role in roles:
        if role.name == "OWNER":
            pass
        else:
            buttons.append(InlineKeyboardButton(
                text=f"{role.name}",
                callback_data=f"{role.name}"
            ))

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()


async def keyboard_choise_vendor() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    vendors = Vendor
    for vendor in vendors:
        buttons.append(InlineKeyboardButton(
            text=f"{vendor.name}",
            callback_data=f"{vendor.name}"
        ))
    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()


async def keyboard_all_order_from_user(data) -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    user = await UserActions.get_user(data)
    orders = await OrdersActions.get_orders_with_customer(user)

    if not orders:
        return False
    for order in orders:
        buttons.append(InlineKeyboardButton(
            text=f"{order.id} - {order.customer.fullname}",
            callback_data=f"{order.id}"
        ))

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()
