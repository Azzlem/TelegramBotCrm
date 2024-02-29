from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keybords.keyboards import keyboard_change_order
from service_base_actions import ServiceBaseActions, ServiceBaseActionsOrder
from states.states import FormListOrders
from utils_format import order_with_comments

router = Router()


@router.message(Command(commands='get_order'))
async def get_order(message: Message, state: FSMContext):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ['admin', 'user']:
        keyboard = await keyboard_change_order(message.from_user)
        await message.answer(
            text="Выберите заказ",
            reply_markup=keyboard
        )
        await state.set_state(FormListOrders.order_id)
    else:
        await message.answer("У вас нет на это прав!")
        await state.clear()


@router.callback_query(StateFilter(FormListOrders.order_id),
                       F.data.in_([str(el) for el in range(1500)]))
async def get_order_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(order_id=int(callback.data))
    await callback.message.delete()
    state_data = await state.get_data()

    data = await ServiceBaseActionsOrder.order(state_data)

    if not data:
        await callback.answer(
            "You have not entered any orders."
        )
        await state.clear()
    else:
        result = await order_with_comments(data)
        print(result)
        await callback.message.answer(result)
        await state.clear()
