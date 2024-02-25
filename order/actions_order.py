from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from OrderActionsBase import OrderService
from service import Service
from utils_format import format_data_order_get

actions_order = Router()


@actions_order.message(Command(commands=["list_orders"]))
async def process_list_orders(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
        date = await OrderService.get_orders(message.from_user.id)
        print(date)
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
