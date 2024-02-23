from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service import Service


async def keyboard_create_order_user() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    users = await Service.get_all_users()
    for user in users:
        buttons.append(InlineKeyboardButton(
            text=f"{user.name}",
            callback_data=f"{user.id}"
        ))

    kb_builder.row(*buttons, width=8)

    return kb_builder.as_markup()
