from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from formatting.user_formatting import DataObject
from keybords.keyboard_list_orders import keyboard_list_orders_status, keyboard_list_order_details, \
    keyboard_list_order_details_another_var, keyboard_choice_options_to_order, keyboard_choice_user, \
    keyboard_status_order
from models.enums import Status
from permission import is_registered, is_owner_admin_user, is_owner_admin, is_user
from states.states_orders import FormListOrderForStatus

router = Router()


@router.message(Command(commands=["list"]))
async def create_order(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_registered(user):
        await message.answer(text="Обратитсь к администратору за активацией вашего профиля")
    elif await is_owner_admin_user(user):
        keyboard = await keyboard_list_orders_status()
        await message.answer(text="ВЫБРАТЬ СТАТУС ЗАКАЗА?", reply_markup=keyboard)
        await state.set_state(FormListOrderForStatus.choise_status)
        await state.update_data(user=user)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_status),
                       F.data.in_([status.name for status in Status]))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status=callback.data)
    await callback.message.delete()
    data = await state.get_data()

    user = data['user']
    status = data['status']

    if await is_owner_admin(user):
        user = None
        orders = await OrdersActions.get_all_orders_accepted(user, status)
        keyboard, text = await keyboard_list_order_details_another_var(orders)
        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )
        if text == "Нет заказов":
            await state.clear()
        else:
            await state.set_state(FormListOrderForStatus.order)
    elif await is_user(user):
        orders = await OrdersActions.get_all_orders_accepted(user, status)
        keyboard, text = await keyboard_list_order_details_another_var(orders)
        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )
        if text == "Нет заказов":
            await state.clear()
        else:
            await state.set_state(FormListOrderForStatus.order)


@router.callback_query(StateFilter(FormListOrderForStatus.order), F.data == 'exit')
async def callback_query_order_exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Ну и ладно!")
    await state.clear()


@router.callback_query(StateFilter(FormListOrderForStatus.order), F.data.isdigit())
async def callback_query_order(callback: CallbackQuery, state: FSMContext):
    await state.update_data(order_id=int(callback.data))
    await callback.message.delete()

    keyboard = await keyboard_choice_options_to_order(callback.from_user)

    await callback.message.answer(
        text="Что будем делать с заказом?",
        reply_markup=keyboard
    )
    await state.set_state(FormListOrderForStatus.choise_action)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "user")
async def callback_query_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    keyboard = await keyboard_choice_user()
    await callback.message.answer(
        text="Выберите инженера",
        reply_markup=keyboard
    )
    await state.set_state(FormListOrderForStatus.appoint)


@router.callback_query(StateFilter(FormListOrderForStatus.appoint))
async def callback_query_appoint(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await state.update_data(user_id=int(callback.data))
    data = await state.get_data()
    data = DataObject(data)
    user = await UserActions.get_user_from_id(data)
    order = await OrdersActions.get_order(data.order_id)
    answer_add_user = await OrdersActions.appoint_user_to_order(data.user_id, data.order_id)
    answer_add_status = await OrdersActions.status_order(Status.APPOINTED, data.order_id)
    if answer_add_user and answer_add_status:
        await bot.send_message(user.telegram_id, text=f"Вы {user.username}\n"
                                                      f"Назначены на заказ №{order.id}\n"
                                                      f"Имя клиента: {order.customer.fullname}\n"
                                                      f"Адрес:  {order.customer.address}\n"
                                                      f"Техника: {order.items[0].vendor} - {order.items[0].model}\n"
                                                      f"Неисправность: {order.items[0].defect}\n")
    await state.clear()


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "exit")
async def callback_query_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Ну и ладно"
    )
    await state.clear()


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "detail")
async def callback_query_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    order = await OrdersActions.get_all_info_order(data['order_id'])
    str_items = ''
    for item in order.items:
        str_items += f"Марка - {item.vendor}\nМодель - {item.model}\nНеисправность - {item.defect}\n"

    await callback.message.answer(
        text=f"Заказ номер: {order.id}\n"
             f"ФИО клиента: {order.customer.fullname}\n"
             f"Телефон клиента: {order.customer.phone}\n"
             f"Адрес клиента: {order.customer.address}\n"
             f"{str_items}"
             f"{order.components}\n"
             f"{order.comments}"
    )
    await state.clear()


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "status")
async def callback_query_status(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    keyboard = await keyboard_status_order(callback.from_user)
    await callback.message.answer(
        text="Выберите новый статус заказа",
        reply_markup=keyboard
    )
    await state.set_state(FormListOrderForStatus.choise_status_final)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_status_final),
                       F.data.in_([status.name for status in Status]))
async def callback_query_status_final(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    answer = await OrdersActions.status_order(callback.data, int(data['order_id']))
    if answer:
        await callback.message.answer(text=f"Статус заказа: {data['order_id']} - изменён на: {callback.data}")
        await state.clear()
    else:
        await callback.message.answer(text="Что то пошло не так, напиши @Azzlem")