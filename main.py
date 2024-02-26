from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand

from UserActionsBase import UserService
from settings import settings
from handlers import (base_handlers, user_handlers,
                      form_del_user, form_change_perm_user, order_handlers, form_change_order, form_create_order)

TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
storage = MemoryStorage()


@dp.message(CommandStart())
async def main_menu(message: Message):
    if await UserService.valid_user(message.from_user.id) in ["admin"]:
        print("admin")
        main_menu_commands = [
            BotCommand(command='help', description='Справка'),
            BotCommand(command='cancel', description='Выход'),
            BotCommand(command='reg', description='Регистрация'),
            BotCommand(command='list_user', description='Инженеры'),
            BotCommand(command='change_perms', description='Изменить пользователя!'),
            BotCommand(command='del_user', description='Удалить пользователя'),
            BotCommand(command='list_orders', description='Список заказов'),
            BotCommand(command='order', description='Создать заказ'),
            BotCommand(command='change_order', description='Изменить заказ'),
        ]
        await bot.set_my_commands(main_menu_commands)

    elif await UserService.valid_user(message.from_user.id) in ["user"]:
        print("not admin")
        main_menu_commands = [
            BotCommand(command='help', description='Справка'),
            BotCommand(command='reg', description='Регистрация'),
            BotCommand(command='list_orders', description='Список заказов'),
            BotCommand(command='order', description='Создать заказ'),
            BotCommand(command='change_order', description='Изменить заказ')
        ]
        await bot.set_my_commands(main_menu_commands)
    else:
        main_menu_commands = [
            BotCommand(command='reg', description='Регистрация'),
        ]
        await bot.set_my_commands(main_menu_commands)
    await message.answer(
        "Ну здарова"
    )


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    if await UserService.valid_user(message.from_user.id) in ["admin", "user"]:
        await message.answer(
            text='Вы вышли из машины состояний\n\n'
                 'Чтобы перейти к заполнению заказа - \n'
                 'отправьте команду /order\n\n'
                 'Чтобы перейти к изменению прав пользователя - \n'
                 'отправьте команду /change_perms\n\n'
                 'Чтобы перейти к списку пользователей - \n'
                 'отправьте команду /list_user \n\n'
        )
        # Сбрасываем состояние и очищаем данные, полученные внутри состояний
        await state.clear()
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


dp.include_router(base_handlers.router)
dp.include_router(user_handlers.router)
dp.include_router(form_del_user.router)
dp.include_router(form_change_perm_user.router)
dp.include_router(order_handlers.router)
dp.include_router(form_change_order.router)
dp.include_router(form_create_order.router)

if __name__ == '__main__':
    dp.run_polling(bot)
