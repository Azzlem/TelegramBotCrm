from aiogram.types import BotCommand

admin_commands = main_menu_commands = [
    BotCommand(command='cancel', description='Выход'),
    BotCommand(command='reg', description='Регистрация'),
    BotCommand(command='list_user', description='Инженеры'),
    BotCommand(command='change_perms', description='Изменить пользователя!'),
    BotCommand(command='deluser', description='Удалить пользователя'),
    BotCommand(command='listuser', description='Инженеры'),
    BotCommand(command='customer_add', description='Создать клиента')

]

user_commands = [
    BotCommand(command='cancel', description='Выход'),
    BotCommand(command='reg', description='Регистрация')
]
ungerister_user_commands = [BotCommand(command='reg', description='Регистрация')]
