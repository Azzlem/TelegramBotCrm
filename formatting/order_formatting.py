async def orders_all(orders):
    answer = ''
    for order in orders:
        answer += (f"Номер заказа: {order.id}\n"
                   f"ФИО: {order.customer.fullname}\n"
                   f"Адрес: {order.customer.address}\n"
                   f"Телефон: {order.customer.phone}\n"
                   f"Инженер: {order.user.fullname}\n"
                   f"Цена заказа: {order.price}\n\n")

    return answer
