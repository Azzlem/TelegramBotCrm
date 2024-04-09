from typing import Dict, List, Tuple

from aiogram.types import User
from aiogram_dialog import DialogManager

from actions_base.actions_orders import OrdersActions
from actions_base.actions_users import UserActions
from models.enums import Status
from models.models import Vendor, Customers, Orders, Users
from permission import is_owner_admin, is_user
from settings import rus_name_status


async def vendor_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    vendor_list = [(vendor.name, vendor.name) for vendor in Vendor]
    return {'elems': vendor_list}


async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user: Users = await UserActions.get_user(event_from_user)
    if await is_owner_admin(user):
        users = await UserActions.get_all_users()
        list_user = [(user.fullname, user.id) for user in users] + [("Не назначать", None)]
    elif await is_user(user):
        list_user = [(user.fullname, user.id)]
    else:
        list_user = []
    return {'elems': list_user}


async def customers_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    customers: list[Customers] = dialog_manager.dialog_data.get('customers_model')
    customer_list = [(customer.fullname, customer.id) for customer in customers]
    return {'elems': customer_list}


async def orders_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> Dict:
    orders: List[Orders] = dialog_manager.dialog_data.get('orders')
    order_list = [
        (f"{order.id}" + (f"-{order.customer.fullname}" if order.customer else ""), order.id)
        for order in orders
    ]
    return {"elems": order_list}


async def status_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs) -> Dict:
    user: Users = await UserActions.get_user(event_from_user)
    rus_name_status_user = rus_name_status[2:6]
    order: Orders = await OrdersActions.get_order(int(dialog_manager.dialog_data.get('order_id')))
    if order.status == Status.CLOSED:
        return {'elems': [("Нельзя менять статус", "exit")]}
    if await is_user(user):
        status_list = [(text, status.name) for status, text in zip(Status, rus_name_status_user)]
        return {'elems': status_list}
    elif await is_owner_admin(user):
        status_list = [(text, status.name) for status, text in zip(Status, rus_name_status)]
        return {'elems': status_list}
