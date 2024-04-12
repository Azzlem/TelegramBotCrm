from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput


async def incorrect_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
                            error: ValueError):
    await message.answer(
        text='Вы ввели что-то не то. Попробуйте еще раз'
    )