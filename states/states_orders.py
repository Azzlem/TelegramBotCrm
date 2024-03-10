from aiogram.fsm.state import StatesGroup, State


class FormAddOrder(StatesGroup):
    fullname = State()
    customer_id = State()
    user_id = State()


class FormDetailOrder(StatesGroup):
    order_id = State()
    status = State()

