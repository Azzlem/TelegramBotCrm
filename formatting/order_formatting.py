async def orders_all(orders):
    answer = ''
    for order in orders:
        if order.customer is None:
            answer += (f"Номер заказа: {order.id}\n"
                       f"Инженер: {order.user.fullname}\n"
                       f"Цена заказа: {order.price}\n\n")
        elif order.user is None:
            answer += (f"Номер заказа: {order.id}\n"
                       f"ФИО: {order.customer.fullname}\n"
                       f"Адрес: {order.customer.address}\n"
                       f"Телефон: {order.customer.phone}\n"
                       f"Инженер: не назначен\n"
                       f"Цена заказа: {order.price}\n\n")
        elif order.user is None and order.customer is None:
            answer += (f"Номер заказа: {order.id}\n"
                       f"Цена заказа: {order.price}\n\n")
        else:
            answer += (f"Номер заказа: {order.id}\n"
                       f"ФИО: {order.customer.fullname}\n"
                       f"Адрес: {order.customer.address}\n"
                       f"Телефон: {order.customer.phone}\n"
                       f"Инженер: {order.user.fullname}\n"
                       f"Цена заказа: {order.price}\n\n")

    return answer
