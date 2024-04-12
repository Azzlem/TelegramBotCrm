from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.check_def import name_check, only_num_check
from handlers.dialog_p.correct_handler_order import correct_component_name_handler, correct_component_price_handler
from handlers.dialog_p.dialog_states import Component
from handlers.dialog_p.icorrect_handlers import incorrect_handler
from utils import dowmload_image


async def get_photo_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(dialog_manager.start_data)
    bot = dialog_manager.middleware_data.get('bot')
    url = await dowmload_image(message, bot)
    dialog_manager.dialog_data['path_photo'] = url
    await dialog_manager.switch_to(Component.get_name)


dialog_components = Dialog(
    Window(
        Const('Загрузите фото чека'),
        MessageInput(
            func=get_photo_handler,
            content_types=ContentType.PHOTO,
        ),
        Button(Const('Назад'), id='back1', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Component.get_photo_receipt
    ),
    Window(
        Const('Напишите название запчасти'),
        TextInput(
            id='component_name',
            type_factory=name_check,
            on_success=correct_component_name_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Назад'), id='back2', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Component.get_name
    ),
    Window(
        Const('Напишите цену'),
        TextInput(
            id='component_price',
            type_factory=only_num_check,
            on_success=correct_component_price_handler,
            on_error=incorrect_handler,
        ),
        Button(Const('Назад'), id='back3', on_click=dialog_base_def.go_back),
        Button(Const('Вернуться в главное меню'), id='exit_button', on_click=dialog_base_def.go_start),
        state=Component.get_price
    )
)
