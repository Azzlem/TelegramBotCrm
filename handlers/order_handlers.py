from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from OrderActionsBase import OrderService
from service_base_actions import ServiceBaseActions, ServiceBaseActionsOrder
from utils_format import format_data_order_get, get_comments_from_user

router = Router()


@router.message(Command(commands=["list_orders"]))
async def process_list_orders(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
        date = await OrderService.get_orders(message.from_user.id)
        # comments = await ServiceBaseActionsOrder.get_comments(date)
        if not date:
            await message.answer(
                "You have not entered any orders."
            )
        else:
            date_formatting = await format_data_order_get(date)
            await message.answer(date_formatting)
            await message.delete()
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


@router.message(Command(commands=["orders"]))
async def process_orders(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
        date = await ServiceBaseActionsOrder.get_comments(message.from_user.id)
        if not date:
            await message.answer(
                "You have not entered any orders."
            )
        else:
            date_formatting = await get_comments_from_user(date)
            await message.answer(date_formatting)
