from aiogram.fsm.state import StatesGroup, State


class FormChangePermsUser(StatesGroup):
    user_id = State()
    role = State()


class FormDeleteUser(StatesGroup):
    user_id = State()


class FormDetailUser(StatesGroup):
    user_id = State()
