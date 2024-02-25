from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, BotCommand
from order.actions_order import actions_order
from order.form_change_order import router_order_change
from order.form_create_order import router_order_create
from service import Service
from settings import settings
from users.actions_users import user_actions
from users.form_change_perm_user import change_perm_user
from users.form_del_user import delete_user

TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
storage = MemoryStorage()


@dp.message(Command(commands=['start']))
async def main_menu(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin"]:
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
    elif await Service.valid_user(message.from_user.id) in ["user"]:
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


@dp.message(Command(commands='help'))
async def process_help(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
        await message.answer(
            f"Это бот база\n"
            f"Команды в боте:\n\n"
            f"Блок USER:\n"
            f"/reg - регистрация(делается 1 раз привязывет ваш ид телеги\n"
            f"/cancel - выход из диалога с ботом\n"
            f"/list_user - простомотр зарегистрированных пользователей(доступно только админу)\n"
            f"/change_perms - изменить права доступа(доступно только админу)\n"
            f"/del_user - удалить юзера(пока просто удаляет без запрета на регистрацию)\n\n\n"
            f"Блок заказы:\n"
            f"/order - создать заказ\n"
            f"/list_orders - просмотреть заказы(доступно пользователям которым админ дал права)\n"
            f"/change_order - изменить существующий заказ."
        )
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
        await message.answer(
            text='Отменять нечего. Вы вне машины состояний\n\n'
                 'Чтобы перейти к заполнению заказа - \n'
                 'отправьте команду /order\n\n'
                 'Чтобы перейти к изменению прав пользователя - \n'
                 'отправьте команду /change_perms\n\n'
                 'Чтобы перейти к списку пользователей - \n'
                 'отправьте команду /list_user \n\n'
        )
    else:
        await message.answer(
            "Обратитесь к Администратору для активации вашего пользователя"
        )


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    if await Service.valid_user(message.from_user.id) in ["admin", "user"]:
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


dp.include_router(router_order_create)
dp.include_router(user_actions)
dp.include_router(router_order_change)
dp.include_router(change_perm_user)
dp.include_router(delete_user)
dp.include_router(actions_order)

if __name__ == '__main__':
    dp.run_polling(bot)
