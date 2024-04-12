from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from actions_base.actions_comments import CommentActions
from actions_base.actions_users import UserActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.check_def import defect_check
from handlers.dialog_p.dialog_states import Comment
from handlers.dialog_p.icorrect_handlers import incorrect_handler
from models.models import Users


async def correct_add_comment(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
                              text: str) -> None:
    dialog_manager.dialog_data["text"] = text
    dialog_manager.dialog_data.update(dialog_manager.start_data)
    user: Users = await UserActions.get_user(message.from_user)

    await CommentActions.create(
        text,
        int(dialog_manager.dialog_data.get('order_id')),
        int(user.id)
    )
    await message.answer(text="Комментарий успешно добавлен")
    await dialog_manager.done()

dialog_comments = Dialog(
    Window(
        Const('Напишите комментарий к заказу'),
        TextInput(
            id='comment_text',
            type_factory=defect_check,
            on_success=correct_add_comment,
            on_error=incorrect_handler,
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=Comment.get_comments
    ),

)
