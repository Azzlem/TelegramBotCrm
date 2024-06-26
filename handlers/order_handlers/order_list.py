import os
from typing import Callable

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PhotoSize, FSInputFile

from actions_base.actions_comments import CommentActions
from actions_base.actions_components import ComponentActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from formatting.user_formatting import DataObject
from keybords.keyboard_list_orders import (keyboard_list_orders_status, keyboard_list_order_details_another_var,
                                           keyboard_choice_options_to_order, keyboard_choice_user, keyboard_status_order
                                           )
from models.enums import Status
from models.models import Role
from settings import PHOTO_FOLDER_PATH
from states.states_orders import FormListOrderForStatus
from utils import dowmload_image

router = Router()


def decorator_permissions(func: Callable) -> Callable:
    async def wrapper(message: Message, state: FSMContext):
        user = await UserActions.get_user(message.from_user)
        if user.role == Role.REGISTERED:
            await message.answer("Обратитсь к администратору за активацией вашего профиля")
        elif user.role not in (Role.ADMIN, Role.OWNER, Role.USER):
            await message.answer("Доступ запрещён")
        else:
            await func(message, state)

    return wrapper


@router.message(Command(commands=["list"]))
@decorator_permissions
async def create_order(message: Message, state: FSMContext):
    keyboard = await keyboard_list_orders_status()
    user = await UserActions.get_user(message.from_user)
    await message.answer(text="ВЫБРАТЬ СТАТУС ЗАКАЗА?", reply_markup=keyboard)
    await state.set_state(FormListOrderForStatus.choise_status)
    await state.update_data(user=user)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_status),
                       F.data == "exit")
async def accept_order_exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Ну и ладно!")
    await state.clear()


@router.callback_query(StateFilter(FormListOrderForStatus.choise_status),
                       F.data.in_([status.name for status in Status]))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    await state.update_data(status=callback.data)
    await callback.message.delete()
    data = await state.get_data()
    user = data['user']
    status = data['status']
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

    keyboard = await keyboard_choice_options_to_order(callback.from_user, int(callback.data))

    await callback.message.answer(
        text="Что будем делать с заказом?",
        reply_markup=keyboard
    )
    await state.set_state(FormListOrderForStatus.choise_action)


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "component")
async def callback_query_component_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Добавьте фото чека")
    await state.set_state(FormListOrderForStatus.component)


@router.message(StateFilter(FormListOrderForStatus.component), F.photo[-1].as_('largest_photo'))
async def callback_query_component_order(message: Message, state: FSMContext, largest_photo: PhotoSize, bot: Bot):
    try:
        path_file = await dowmload_image(message, bot)
        await state.update_data(path_photo=path_file)
        await state.set_state(FormListOrderForStatus.name_component_else)
        await message.answer(text="Введите название запчасти")
    except:
        await message.answer(text='Обратитесь к администратору @Azzlem')
        await state.clear()


@router.message(StateFilter(FormListOrderForStatus.name_component_else))
async def callback_query_name_component_order(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Введите цену")
    await state.set_state(FormListOrderForStatus.price_component)


@router.message(StateFilter(FormListOrderForStatus.price_component), F.text.isdigit())
async def callback_query_price_component_order(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    data = await state.get_data()
    data = DataObject(data=data)
    await ComponentActions.create(data.name, data.path_photo, data.order_id, data.price)
    await message.answer(text="Запчасть добавлена")


@router.message(StateFilter(FormListOrderForStatus.price_component))
async def callback_query_price_component_order(message: Message, state: FSMContext):
    await message.answer(text=f"Это не цыфра, или ты заплатил {message.text} рублей?")


@router.message(StateFilter(FormListOrderForStatus.component))
async def warning_not_photo(message: Message):
    await message.answer(
        text='Пожалуйста, на этом шаге отправьте '
             'ваше фото\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel'
    )


@router.callback_query(StateFilter(FormListOrderForStatus.choise_action), F.data == "comment")
async def callback_query_comment_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text="Напишите комментарий")
    await state.set_state(FormListOrderForStatus.comment)


@router.message(StateFilter(FormListOrderForStatus.comment))
async def callback_query_comment_order_write(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    comment = await CommentActions.create(data["comment"], int(data["order_id"]), data['user'].id)
    await message.answer(text=f"Коментарий '{comment}' успешно добавлен.")
    await state.clear()


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
                                                      f"Техника: {order.items[0].vendor.name} - {order.items[0].model}\n"
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
async def callback_query_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    data = await state.get_data()
    order = await OrdersActions.get_all_info_order(data['order_id'])
    text = (f"Заказ номер: {order.id}\n"
            f"ФИО клиента: {order.customer.fullname}\n"
            f"Телефон клиента: {order.customer.phone}\n"
            f"Адрес клиента: {order.customer.address}\n"
            f"\nСписок Техники клиента:\n")
    for item in order.items:
        text += f"{item.vendor.name} модель: {item.model}\nНеисправность: {item.defect}\n"
    text += "\nСписок компонентов:\n"
    for component in order.components:
        text += f"{component.name} - {component.price}\n"
    text += "\nСписок комментариев:\n"
    comments = await CommentActions.get_comments_by_order_id(order.id)
    for comment in comments:
        text += f"{comment.owner.fullname} - {comment.text} - {comment.created_on.strftime('%d-%m-%Y %H-%M')}\n"
    await callback.message.answer(text=text)
    for comment_foto in order.components:
        photo = FSInputFile(f"{PHOTO_FOLDER_PATH}/{comment_foto.path_photo}")
        await bot.send_photo(callback.from_user.id, photo)
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
