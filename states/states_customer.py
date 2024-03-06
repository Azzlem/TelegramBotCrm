from aiogram.fsm.state import StatesGroup, State


class FormAddCustomer(StatesGroup):
    fullname = State()
    phone = State()
    address = State()


class FormUpdateCustomer(StatesGroup):
    id = State()
    choice = State()
    fullname = State()
    phone = State()
    address = State()
    email = State()


