from typing import List, Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from actions_base.actions_users import UserActions
from models.models import Orders, Components, Role
from settings import rus_name_status


async def format_text(order: Orders) -> str:
    items = "\n".join(f'{item.vendor.name} - {item.model}' for item in order.items)
    comments = "\n".join(comment.text for comment in order.comments)
    components = "\n".join(f"{component.name} - {component.price}" for component in order.components)
    components_new: List[Components] = order.components
    spending = sum(component_new.price for component_new in components_new)
    comments_formatted = "\n".join(f"{i + 1}. {comment}" for i, comment in enumerate(comments.split("\n")))
    text = f"""

<b>Заказ номер:</b> {order.id}

<b>Клиент:</b> {order.customer.fullname}
<b>Телефон:</b> {order.customer.phone}
<b>Адрес:</b> {order.customer.address}

<b>Инженер:</b> {order.user.fullname if order.user else "Не назначен"}

<b>Техника:</b>
{items if order.items else "Без техники"}

...

<b>Комментарии по заказу:</b>
{comments_formatted}

...

<b>Запчасти в заказе:</b>
{components if components else "Нет запчастей"}

<b>Затраты:</b> {spending}
<b>Оплачено:</b> {order.price}
<b>Прибыль:</b> {order.price - spending}

<b>Статус:</b> {rus_name_status[order.status.value]}
"""
    return text

