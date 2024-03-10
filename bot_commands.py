from aiogram.types import BotCommand

admin_commands = main_menu_commands = [
    BotCommand(command='cancel', description='Выход'),
    BotCommand(command='reg', description='Регистрация'),
    BotCommand(command='list_user', description='Инженеры'),
    BotCommand(command='change_perms', description='Изменить пользователя!'),
    BotCommand(command='deluser', description='Удалить пользователя'),
    BotCommand(command='listuser', description='Инженеры'),
    BotCommand(command='customer_add', description='Создать клиента'),
    BotCommand(command='customer_edit', description='Изменить клиента'),
    BotCommand(command='item_add', description='Добавить технику (если у вас есть клиент)'),
    BotCommand(command='order_add', description='Создать заказ'),
    BotCommand(command='list_orders', description='Список заказов')

]

user_commands = [
    BotCommand(command='cancel', description='Выход'),
    BotCommand(command='reg', description='Регистрация'),
    BotCommand(command='customer_add', description='Создать клиента'),
    BotCommand(command='item_add', description='Добавить технику (если у вас есть клиент)'),
    BotCommand(command='order_add', description='Создать заказ'),
    BotCommand(command='list_orders', description='Список заказов')

]
ungerister_user_commands = [BotCommand(command='reg', description='Регистрация')]
