from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from service_base_actions import ServiceBaseActions

router = Router()


@router.message(Command(commands='help'))
async def process_help(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
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


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    if await ServiceBaseActions.valid_user(message.from_user.id) in ["admin", "user"]:
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


