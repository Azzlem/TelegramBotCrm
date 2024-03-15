from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.enums import Status


async def keyboard_list_orders_status() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    temp = ["ПРИНЯТ", "НАЗНАЧЕН", "В РАБОТЕ", "ТЕХНИКА В СЦ", "ОПЛАЧЕН", "ВЫДАН", "ЗАКРЫТ"]
    buttons.append(InlineKeyboardButton(text=temp[0], callback_data=Status.ACCEPTED.name))
    buttons.append(InlineKeyboardButton(text=temp[1], callback_data=Status.APPOINTED.name))
    buttons.append(InlineKeyboardButton(text=temp[2], callback_data=Status.IN_WORK.name))
    buttons.append(InlineKeyboardButton(text=temp[3], callback_data=Status.DEVICE_IN_SERVICE.name))
    buttons.append(InlineKeyboardButton(text=temp[4], callback_data=Status.PAID.name))
    buttons.append(InlineKeyboardButton(text=temp[5], callback_data=Status.ISSUED_TO_CUSTOMER.name))
    buttons.append(InlineKeyboardButton(text=temp[6], callback_data=Status.CLOSED.name))

    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


async def keyboard_list_order_details(orders) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if not orders:
        kb_builder.row(*buttons, width=2)
        return kb_builder.as_markup()

    for order in orders:
        str_items = ''
        for item in order.items:
            str_items += f"{item.vendor.name}-{item.model}-{item.defect}"
        buttons.append(InlineKeyboardButton(
            text=f"{order.id}-{order.customer.address}-{len(order.items)}-{str_items}",
            callback_data=str(order.id)
        )
        )

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


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
            items_str += f"{item.vendor} - {item.model} - {item.defect}"
        text += f"Номер заказа: {el.id}\nКлиент: {el.customer.fullname}\nАдрес: {el.customer.address}\n{items_str}\n\n"

    kb_builder.row(*buttons, width=8)
    return [kb_builder.as_markup(), text]


async def keyboard_choice_options_to_order() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text="Назначить инженера", callback_data="user"),
                                           InlineKeyboardButton(text="Посмотреть подробности", callback_data="detail"),
                                           InlineKeyboardButton(text="Выйти", callback_data="exit")]

    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()
