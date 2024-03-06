from aiogram.fsm.state import StatesGroup, State


class FormAddItem(StatesGroup):
    vendor = State()
    model = State()
    defect = State()
    order_id = State()
