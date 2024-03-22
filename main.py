import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommandScopeChat

from actions_base.actions_users import UserActions
from bot_commands import admin_commands, user_commands, ungerister_user_commands
from handlers.customer_handlers import fsm_add_customer, fsm_edit_customer
from handlers.item_handlers import fsm_add_item
from handlers.order_handlers import order_create, order_list

from settings import settings, string_cancel
from handlers import base_handlers
from handlers.user_handlers import user_change_permission, user_delete, user_list, user_handlers

from aiogram_dialog import Window, Dialog, DialogManager, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

storage = MemoryStorage()
TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def main_menu(message: Message):
    user = await UserActions.get_user(message.from_user)
    if not user:
        main_menu_commands = ungerister_user_commands
        await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("Ну здарова")

    elif user.role.name == "REGISTERED":
        main_menu_commands = ungerister_user_commands
        await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("Добро пожаловать , обратитесь к администратору для получения прав")

    elif user.role.name == 'USER':
        main_menu_commands = user_commands
        await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("добро пожаловать , хорошего дня!")

    elif user.role.name == 'ADMIN':
        main_menu_commands = admin_commands
        await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("Здарова Админ! ОпяТь работа?")

    elif user.role.name == 'OWNER':
        main_menu_commands = admin_commands
        await bot.set_my_commands(main_menu_commands, BotCommandScopeChat(chat_id=message.from_user.id))
        await message.answer("Новые фичи привез да? Опять все ломать будешь?")


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if user.role.name in ['ADMIN', 'OWNER', 'USER']:
        await message.answer(
            text=string_cancel
        )
        await state.clear()
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


class MySG(StatesGroup):
    main = State()


main_window = Window(
    Const("Hello, unknown person"),  # just a constant text
    Button(Const("Useless button"), id="nothing"),  # button with text and id
    state=MySG.main,  # state is used to identify window between dialogs
)

dialog = Dialog(main_window)
setup_dialogs(dp)


@dp.message(Command("root"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


dp.include_router(dialog)
dp.include_router(base_handlers.router)

# Хендлеры Пользователя
dp.include_router(user_handlers.router)
dp.include_router(user_list.router)
dp.include_router(user_delete.router)
dp.include_router(user_change_permission.router)

# Хендлеры Клиента
dp.include_router(fsm_add_customer.router)
dp.include_router(fsm_edit_customer.router)

# Хендлеры техники
dp.include_router(fsm_add_item.router)

# Хендлеры заказа
dp.include_router(order_create.router)
dp.include_router(order_list.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
