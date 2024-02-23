import asyncio

from sqlalchemy import select

from base import async_session_maker
from order.models import Order
from service import Service


async def format_data_order_get(data: list):
    answer = ''
    for order in data:
        answer += (f'Номер заказа: {order.id}\n'
                   f'Имя клиента: {order.client_name}\n'
                   f'Телефон клиента: {order.client_phone}\n'
                   f'Техника клиента: {order.device}\n'
                   f'Неисправность: {order.mulfunction}\n\n\n\n')
    return answer
