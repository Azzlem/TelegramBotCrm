from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    menu = State()


class Customer(StatesGroup):
    customer = State()
    find = State()
    list_customer = State()
    list_customer_choice = State()
    list_order = State()


class Order(StatesGroup):

    order_start = State()
    create_order = State()
    create_customer = State()
    create_customer_phone = State()
    create_customer_address = State()
    choice_vendor = State()
    model_item = State()
    defect = State()
    user_add = State()
    user_choice = State()
