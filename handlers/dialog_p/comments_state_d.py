from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from actions_base.actions_comments import CommentActions
from actions_base.actions_users import UserActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.check_def import not_only_num_check
from handlers.dialog_p.orders import incorrect_handler
from models.models import Users


# class Comment(StatesGroup):
#     get_comments = State()


# async def start_add_comment(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.start(Comment.get_comments)
#
#
# async def correct_add_comment(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager,
#                               text: str) -> None:
#     dialog_manager.dialog_data["text"] = text
#     user: Users = await UserActions.get_user(message.from_user)
#     await CommentActions.create(
#         text,
#         int(dialog_manager.dialog_data.get('order_id')),
#         int(user.id)
#     )
#     await message.answer(text="Комментарий успешно добавлен")
#     await dialog_manager.done()


# dialog_comments = Dialog(
#     Window(
#         Const('Напишите комментарий к заказу'),
#         TextInput(
#             id='comment_text',
#             type_factory=defect_check,
#             on_success=correct_add_comment,
#             on_error=incorrect_handler,
#         ),
#         Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
#         state=Comment.get_comments
#     ),
#
# )
