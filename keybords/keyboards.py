from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from actions_base.actions_users import UserActions
from models.users import Role


async def keyboard_list_user(data) -> InlineKeyboardMarkup:
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
