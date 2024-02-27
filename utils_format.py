import asyncio

from base import async_session_maker
from order.models import Order


async def format_data_order_get(data: list):
    answer = ''

    for order in data:
        status = order.user_id if order.user_id is not None else 'Нераспределен'
        answer += (f'Номер заказа: {order.id}\n'
                   f'Имя клиента: {order.client_name}\n'
                   f'Телефон клиента: {order.client_phone}\n'
                   f'Техника клиента: {order.device}\n'
                   f'Неисправность: {order.mulfunction}\n'
                   f'{status}\n\n\n')

    return answer


async def format_data_user_get(data: list):
    answer = ''

    for user in data:
        status = ''
        if user.status == 0:
            status = "Не авторизован"
        if user.status == 1:
            status = "Инженер"
        if user.status == 2:
            status = "Админ"
        answer += (f'Id user {user.id}\n'
                   f'User Name: {user.name}\n'
                   f'Permissions: {status}\n\n')

    return answer


async def format_data_user_set(data) -> dict:
    data = {
        'tg_user_id': data.id,
        'name': data.username
    }

    return data


async def format_valid_user(data: list):
    if not data:
        return False
    for user in data:
        print(user.status)
        if user.status == 1:
            return "user"
        elif user.status == 2:
            return "admin"
        else:
            return False


async def get_comments_from_order():
    async with async_session_maker() as db:
        order = await db.get(Order, 1)
        comments = order.comments
        for el in comments:
            print(el)


