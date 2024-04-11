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
    input_customer_name = State()
    choice_customer_button = State()
    find_order = State()
    order_action = State()
    actions_choice_orders = State()
    create_component_photo = State()
    create_component_name = State()
    create_component_price = State()
    send_status = State()
    get_my_orders = State()
    my_order_actions = State()


class Comment(StatesGroup):
    get_comments = State()


class Component(StatesGroup):
    get_photo_receipt = State()
    get_name = State()
    get_price = State()


class StatusOrder(StatesGroup):
    get_status = State()
