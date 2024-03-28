from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    menu = State()


class Customer(StatesGroup):
    customer = State()
    find = State()
    list_customer = State()
