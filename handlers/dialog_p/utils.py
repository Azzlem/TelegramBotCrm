from models.models import Orders


async def format_text(order: Orders) -> None:
    items = "\n".join(f'{item.vendor.name} - {item.model}' for item in order.items)
    comments = "\n".join(comment.text for comment in order.comments)
    components = "\n".join(f"{component.name} - {component.price}" for component in order.components)
    spending = sum(component.price for component in order.components)
    comments_formatted = "\n".join(f"{i + 1}. {comment}" for i, comment in enumerate(comments.split("\n")))
    print(f"""
        <b>Заказ номер:</b> {order.id}

        <b>Клиент:</b> {order.customer.fullname}
        <b>Телефон:</b> {order.customer.phone}
        <b>Адрес:</b> {order.customer.address}

        <b>Инженер:</b> {order.user.fullname if order.user else "Не назначен"}

        <b>Техника:</b>
        {items if order.items else "Без техники"}""")
    print(f"""
        ...
        <b>Коментарии по заказу:</b>
        {comments_formatted}""")
    print(f"""
        ...
        <b>Запчасти в заказе:</b>
        {'' if components == '' else components}
        ...""")
    print(f"""
        <b>Затраты:</b> {spending}
        <b>Оплачено:</b> {order.price}
        <b>Прибыль:</b> {order.price - spending}
        """)



