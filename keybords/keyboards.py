from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from models.models import Role, Vendor, Customers
from permission import is_owner_admin, is_user, is_registered


async def keyboard_list_user() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    users = await UserActions.get_all_users()
    for user in users:
        buttons.append(InlineKeyboardButton(
            text=f"{user.fullname}",
            callback_data=f"{user.id}"
        ))
    kb_builder.row(*buttons, width=2)

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
    if user.role.name in ["ADMIN", "OWNER"]:
        orders = await OrdersActions.get_all_orders_with_customer()
        if not orders:
            return False
        for order in orders:
            buttons.append(InlineKeyboardButton(
                text=f"{order.id} - {order.customer.fullname}",
                callback_data=f"{order.id}"
            ))
    else:
        orders = await OrdersActions.get_orders_with_customer(user)
        if not orders:
            buttons.append(InlineKeyboardButton(text="Что то не то", callback_data="Ikzgf"))
        for order in orders:
            buttons.append(InlineKeyboardButton(
                text=f"{order.id} - {order.customer.fullname}",
                callback_data=f"{order.id}"
            ))

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()


async def keyboard_choice_customer_edit() -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    customers = await CustomerActions.get_customers()
    if not customers:
        return False
    for customer in customers:
        buttons.append(
            InlineKeyboardButton(
                text=f"{customer.fullname} | {customer.address}"
                ,
                callback_data=f"{customer.id}"
            )
        )

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


async def keyboard_customer_edit() -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=f"Имя", callback_data="fullname"),
                                           InlineKeyboardButton(text=f"Телефон", callback_data="phone"),
                                           InlineKeyboardButton(text=f"Адресс", callback_data="adress"),
                                           InlineKeyboardButton(text=f"Почта", callback_data="email")]

    kb_builder.row(*buttons, width=4)

    return kb_builder.as_markup()


async def keyboard_choice_customer_filter(data) -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    customers = await CustomerActions.get_customers_for_fullname(data)
    if not customers:
        return False
    for customer in customers:
        buttons.append(
            InlineKeyboardButton(
                text=f"{customer.fullname} | {customer.address}"
                ,
                callback_data=f"{customer.id}"
            )
        )

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


async def keyboard_list_user_for_order(data) -> InlineKeyboardMarkup | bool:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    user_valid = await UserActions.get_user(data)
    if await is_owner_admin(user_valid):
        users = await UserActions.get_all_users()
        for user in users:
            buttons.append(InlineKeyboardButton(
                text=f"{user.fullname}",
                callback_data=f"{user.id}"
            ))
    else:
        buttons.append(InlineKeyboardButton(text=f"{user_valid.fullname}",
                                            callback_data=f"{user_valid.id}"))
    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()
