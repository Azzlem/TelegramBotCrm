from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command(commands='order'))
async def detail_order(message: Message, state: FSMContext):
    pass
