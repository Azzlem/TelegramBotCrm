from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from OrderActionsBase import OrderService
from utils_format import format_data_order_get

actions_order = Router()


@actions_order.message(Command(commands=["list_orders"]))
async def process_list_orders(message: Message):
    date = await OrderService.get_orders(message.from_user.id)
    date_formatting = await format_data_order_get(date)
    await message.answer(date_formatting)
    await message.delete()
