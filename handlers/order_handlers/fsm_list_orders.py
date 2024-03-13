import sys

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from formatting.order_formatting import orders_all
from permission import is_owner_admin, is_user, is_registered

logger.add("file_{time}.json")
router = Router()


@logger.catch
@router.message(Command(commands='list_orders'))
async def list_orders(message: Message):
    try:
        user = await UserActions.get_user(message.from_user)
        if await is_registered(user):
            await message.answer(
                text="Заблудился?    Сходи к Админу! Он разблудит! И нехер тыкать проста так кнопочки.")

        elif await is_user(user):
            orders = await OrdersActions.get_all_orders_with_all_info_for_id(message.from_user)
            orders = await orders_all(orders)
            if len(orders) == 0:
                await message.answer(text="У вас нет активных заказов.")

            else:

                await message.answer(text=orders)

        elif await is_owner_admin(user):
            orders = await OrdersActions.get_all_orders_with_all_info()
            orders = await orders_all(orders)
            await message.answer(text=orders)

        else:
            await message.answer(text="Ненадо тыкать незнакомные команды....это плохо влияет на карму.")
    except:
        logger.add("file_{time}.json")
        await message.answer(text="что то не так")
