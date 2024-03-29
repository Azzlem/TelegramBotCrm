from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    menu = State()


class Customer(StatesGroup):
    customer = State()
    find = State()
    list_customer = State()
    list_customer_choice = State()
    list_order = State()
