from aiogram.fsm.state import StatesGroup, State


class FormOrder(StatesGroup):
    client_name = State()
    client_phone = State()
    device = State()
    mulfunction = State()
    user_id = State()


class FormChangePermsUser(StatesGroup):
    user_id = State()
    role = State()


class FormDeleteUser(StatesGroup):
    user_id = State()


class FormDetailUser(StatesGroup):
    user_id = State()


class FormOrderChange(StatesGroup):
    order_id = State()
    client_name = State()
    client_phone = State()
    device = State()
    mulfunction = State()
    user_id = State()


class FormListOrders(StatesGroup):
    order_id = State()


class FormDetailOrder(StatesGroup):
    pass
