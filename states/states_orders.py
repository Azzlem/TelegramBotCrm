from aiogram.fsm.state import StatesGroup, State


class FormAddOrder(StatesGroup):
    fullname = State()
    customer_id = State()
    user_id = State()


class FormDetailOrder(StatesGroup):
    order_id = State()
    status = State()


class FormCreateOrder(StatesGroup):
    user_id = State()
    user_choice = State()
    address = State()
    phone = State()
    fullname = State()
    defect = State()
    model = State()
    vendor_choice = State()
    choice_customer = State()
    search_customer = State()
    create_or_no = State()


class FormListOrderForStatus(StatesGroup):
    choise_status_final = State()  # изменить статус
    appoint = State()  # назначить
    choise_action = State()  # выбор действия
    choise_status = State()  # выбор статуса
    order = State()  # список заказов
