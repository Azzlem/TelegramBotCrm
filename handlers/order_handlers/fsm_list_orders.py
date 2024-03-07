from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from formatting.order_formatting import orders_all
from models.models import Role, Orders

router = Router()


@router.message(Command(commands='list_orders'))
async def list_orders(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if not user:
        await message.answer(text='хУЛИ НАДО?')

    elif user.role.name == Role.REGISTERED.name:
        await message.answer(text="Заблудился?    Сходи к Админу! Он разблудит! И нехер тыкать проста так кнопочки.")

    elif user.role.name == Role.USER.name:
        orders = await OrdersActions.get_all_orders_with_all_info_for_id(message.from_user)
        orders = await orders_all(orders)
        await message.answer(text=orders)

    elif user.role.name in [Role.ADMIN.name, Role.OWNER.name]:
        orders = await OrdersActions.get_all_orders_with_all_info()
        orders = await orders_all(orders)
        await message.answer(text=orders)

    else:
        await message.answer(text="Я хуй знает кто ты, напиши мне мой ник в тг Azzlem")
