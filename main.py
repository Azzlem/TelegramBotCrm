from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from service import Service
from settings import settings

TOKEN = settings.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ тестовый бот!')


@dp.message(Command(commands=["registr"]))
async def process_register_command(message: Message):
    await Service.add_user(message.from_user.username, message.from_user.id)
    await message.answer("ёпта")


if __name__ == '__main__':
    dp.run_polling(bot)
