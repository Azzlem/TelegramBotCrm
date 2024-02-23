from aiogram.fsm.state import StatesGroup, State


class FormOrder(StatesGroup):
    client_name = State()
    client_phone = State()
    device = State()
    mulfunction = State()
    user_id = State()


class FormChangePermsUser(StatesGroup):
    user_id = State()
    status = State()


class FormDeleteUser(StatesGroup):
    user_id = State()


class FormOrderChange(StatesGroup):
    id_order = State()
    user_id = State()
    client_name = State()
    client_phone = State()
    device = State()
    mulfunction = State()
