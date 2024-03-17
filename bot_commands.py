from aiogram.types import BotCommand

admin_commands = main_menu_commands = [
    BotCommand(command='create_order', description='Создать заказ'),
    BotCommand(command='list', description='Список заказов'),
    BotCommand(command='customer_add', description='Создать клиента'),
    BotCommand(command='item_add', description='Добавить технику (если у вас есть клиент)'),
    BotCommand(command='cancel', description='Выход'),
    BotCommand(command='list_user', description='Инженеры'),
    BotCommand(command='change_perms', description='Изменить пользователя!'),
    BotCommand(command='customer_edit', description='Изменить клиента'),
]

user_commands = [
    BotCommand(command='create_order', description='Создать заказ'),
    BotCommand(command='list', description='Список заказов'),
    BotCommand(command='item_add', description='Добавить технику (если у вас есть клиент)'),
    BotCommand(command='customer_add', description='Создать клиента'),
    BotCommand(command='cancel', description='Выход')
]
ungerister_user_commands = [BotCommand(command='reg', description='Регистрация')]
