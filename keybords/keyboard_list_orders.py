from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from actions_base.actions_users import UserActions
from models.enums import Status
from permission import is_owner_admin, is_user
from settings import rus_name_status


async def keyboard_list_orders_status() -> InlineKeyboardMarkup:
    buttons = [
                  InlineKeyboardButton(text=text, callback_data=status.name)
                  for status, text in zip(Status, rus_name_status)
              ] + [InlineKeyboardButton(text="Выход", callback_data="exit")]

    return InlineKeyboardBuilder().row(*buttons, width=2).as_markup()


async def keyboard_list_order_details_another_var(orders) -> InlineKeyboardMarkup | list:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if not orders:
        kb_builder.row(*buttons, width=2)
        return [kb_builder.as_markup(), "Нет заказов"]

    for order in orders:
        buttons.append(InlineKeyboardButton(
            text=f"{order.id}",
            callback_data=str(order.id)
        )
        )
    text = ''
    for el in orders:
        items_str = ''
        for item in el.items:
            items_str += f"{item.vendor.name} - {item.model} - {item.defect}"
        text += f"Номер заказа: {el.id}\nКлиент: {el.customer.fullname}\nАдрес: {el.customer.address}\n{items_str}\n\n"
    buttons.append(InlineKeyboardButton(text="Выход", callback_data="exit"))
    kb_builder.row(*buttons, width=8)
    return [kb_builder.as_markup(), text]


async def keyboard_choice_options_to_order(data) -> InlineKeyboardMarkup:
    user = await UserActions.get_user(data)
    buttons = [
        InlineKeyboardButton(text="Посмотреть подробности", callback_data="detail"),
        InlineKeyboardButton(text="Выйти", callback_data="exit"),
        InlineKeyboardButton(text="Изменить статус", callback_data="status"),
        InlineKeyboardButton(text="Добавить комментарий", callback_data="comment")
    ]

    if await is_owner_admin(user):
        buttons.insert(0, InlineKeyboardButton(text="Назначить инженера", callback_data="user"))

    return InlineKeyboardBuilder().row(*buttons, width=2).as_markup()


async def keyboard_choice_user() -> InlineKeyboardMarkup:
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


async def keyboard_status_order(data) -> InlineKeyboardMarkup:
    user = await UserActions.get_user(data)

    if await is_owner_admin(user):
        statuses = [status for status in Status]
    elif await is_user(user):
        statuses = [Status.IN_WORK, Status.DEVICE_IN_SERVICE, Status.ISSUED_TO_CUSTOMER]
    else:
        return InlineKeyboardMarkup()

    buttons = [
        InlineKeyboardButton(text=rus_name_status[status.value], callback_data=status.name)
        for status in statuses
    ]

    return InlineKeyboardBuilder().row(*buttons, width=2).as_markup()
