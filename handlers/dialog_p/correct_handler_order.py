from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from actions_base.actions_comments import CommentActions
from actions_base.actions_components import ComponentActions
from actions_base.actions_customers import CustomerActions
from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from handlers.dialog_p.check_def import name_check, phone_check, address_check, model_check, defect_check
from handlers.dialog_p.dialog_states import Order, Component
from models.models import Users


async def correct_name_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["name"] = name_check(text)
    await dialog_manager.switch_to(Order.create_customer_phone)


async def correct_phone_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["phone"] = phone_check(text)
    await dialog_manager.switch_to(Order.create_customer_address)


async def correct_address_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["address"] = address_check(text)
    await dialog_manager.switch_to(Order.choice_vendor)


async def correct_model_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["model"] = model_check(text)
    await dialog_manager.switch_to(Order.defect)


async def correct_defect_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data["defect"] = defect_check(text)
    await dialog_manager.switch_to(Order.user_choice)


async def correct_customer_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    if all(ch.isdigit() for ch in text):
        customer = [await CustomerActions.get_customer_by_phone(int(text))]
    else:
        customer = await CustomerActions.get_customers_for_fullname(text)
    if customer:
        dialog_manager.dialog_data["customers_model"] = customer
        await dialog_manager.switch_to(Order.choice_customer_button)
    else:
        await message.answer(
            text='Не найден. Попробуйте еще раз'
        )


async def correct_find_order_handler(message: Message,
                                     widget: ManagedTextInput,
                                     dialog_manager: DialogManager,
                                     text: str) -> None:
    if all(ch.isdigit() for ch in text):
        orders = [await OrdersActions.get_order(int(text))]
        if orders[0]:
            dialog_manager.dialog_data["orders"] = orders
            await dialog_manager.switch_to(Order.order_action)
        else:
            customer = await CustomerActions.get_customer_by_phone(int(text))
            if customer:
                orders = await OrdersActions.get_all_orders_to_customer(customer.id)
                dialog_manager.dialog_data["orders"] = orders
                await dialog_manager.switch_to(Order.order_action)
            else:
                await message.answer(
                    text=f"По этому '{text}' номеру клиентов и заказов не найдено.\nПопробуйте ещё раз!")
                await dialog_manager.switch_to(Order.find_order)
    else:
        customer = await CustomerActions.get_customers_for_fullname(text)
        if customer:
            orders = await OrdersActions.get_all_orders_to_customer(customer[0].id)
            dialog_manager.dialog_data["orders"] = orders
            await dialog_manager.switch_to(Order.order_action)
        else:
            await message.answer(text=f"По этому '{text}' имени клиентов и заказов не найдено.\nПопробуйте ещё раз!")
            await dialog_manager.switch_to(Order.find_order)


async def correct_component_name_handler(message: Message,
                                         widget: ManagedTextInput,
                                         dialog_manager: DialogManager,
                                         text: str) -> None:
    dialog_manager.dialog_data["name"] = text
    await dialog_manager.switch_to(Component.get_price)


async def correct_component_price_handler(message: Message,
                                          widget: ManagedTextInput,
                                          dialog_manager: DialogManager,
                                          text: str) -> None:
    dialog_manager.dialog_data["price"] = text
    await ComponentActions.create(
        dialog_manager.dialog_data.get('name'),
        dialog_manager.dialog_data.get('path_photo'),
        int(dialog_manager.dialog_data.get('order_id')),
        int(dialog_manager.dialog_data.get('price')),
    )
    await message.answer(
        text="Запчасть успешно добавлена"
    )
    await dialog_manager.done()

