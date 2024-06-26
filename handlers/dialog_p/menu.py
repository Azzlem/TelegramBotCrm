from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, User
from aiogram_dialog import Window, Dialog, setup_dialogs, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger

from actions_base.actions_users import UserActions
from handlers.dialog_p.customers import customer_dialog
from handlers.dialog_p.dialog_states import Menu, Customer, Order
from handlers.dialog_p.dialog_windows.dialog_comments_window import dialog_comments
from handlers.dialog_p.dialog_windows.dialog_components_window import dialog_components
from handlers.dialog_p.dialog_windows.dialog_status_window import dialog_status
from handlers.dialog_p.orders import order_dialog

router = Router()


async def start_customer(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=Customer.customer)


async def start_order(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=Order.order_start,  mode=StartMode.RESET_STACK)


async def exit_all(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()


async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user = await UserActions.get_user(event_from_user)
    return {'username': user.username}


menu_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('Меню'),
        Row(
            Button(Const('Клиенты'), id='go_customer', on_click=start_customer),
            Button(Const('Заказы'), id='go_order', on_click=start_order),
            Button(Const('Инженеры'), id='go_second', on_click=start_customer),
            Button(Const('Статистика'), id='go_second', on_click=start_customer)
        ),
        Button(Const("Выход"), id='exit', on_click=exit_all),
        getter=user_getter,
        state=Menu.menu
    ),
)

setup_dialogs(router)
router.include_router(menu_dialog)
router.include_router(customer_dialog)
router.include_router(order_dialog)
router.include_router(dialog_comments)
router.include_router(dialog_components)
router.include_router(dialog_status)


@router.message(Command("menu"))
async def start(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.start(Menu.menu, mode=StartMode.RESET_STACK)
    except:
        logger.add("logs/file_{time}.json", rotation="weekly")
        logger.exception("What?!")
