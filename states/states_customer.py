from aiogram.fsm.state import StatesGroup, State


class FormAddCustomer(StatesGroup):
    fullname = State()
    phone = State()
    address = State()
