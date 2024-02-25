from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from order.actions_order import actions_order
from order.form_change_order import router_order_change
from order.form_create_order import router_order_create
from settings import settings
from users.actions_users import user_actions
from users.form_change_perm_user import change_perm_user
from users.form_del_user import delete_user

TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
storage = MemoryStorage()


@dp.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(
        f"Это бот база\n"
        f"Команды в боте:\n\n"
        f"Блок USER:\n"
        f"/registr - регистрация(делается 1 раз привязывет ваш ид телеги\n"
        f"/cancel - выход из диалога с ботом\n"
        f"/list_user - простомотр зарегистрированных пользователей(доступно только админу)\n"
        f"/change_perms - изменить права доступа(доступно только админу)\n"
        f"/del_user - удалить юзера(пока просто удаляет без запрета на регистрацию)\n\n\n"
        f"Блок заказы:\n"
        f"/order - создать заказ\n"
        f"/list_orders - просмотреть заказы(доступно пользователям которым админ дал права)\n"
        f"/change_order - изменить существующий заказ."
    )


@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к заполнению заказа - \n'
             'отправьте команду /order\n\n'
             'Чтобы перейти к изменению прав пользователя - \n'
             'отправьте команду /change_perms\n\n'
             'Чтобы перейти к списку пользователей - \n'
             'отправьте команду /list_user \n\n'
    )


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
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


dp.include_router(router_order_create)
dp.include_router(user_actions)
dp.include_router(router_order_change)
dp.include_router(change_perm_user)
dp.include_router(delete_user)
dp.include_router(actions_order)

if __name__ == '__main__':
    dp.run_polling(bot)
