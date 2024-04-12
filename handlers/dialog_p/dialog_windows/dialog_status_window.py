from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Const, Format

from actions_base.actions_orders import OrdersActions
from handlers.dialog_p import dialog_base_def
from handlers.dialog_p.dialog_states import StatusOrder
from handlers.dialog_p.getters import status_getter


async def select_status(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(dialog_manager.start_data)
    dialog_manager.dialog_data['status_order'] = item_id
    await OrdersActions.status_order(
        dialog_manager.dialog_data.get('status_order'),
        int(dialog_manager.dialog_data.get('order_id')),
    )
    await dialog_manager.done()


dialog_status = Dialog(
    Window(
        Const('Выберите статус'),
        ScrollingGroup(Select(
            Format('{item[0]}'),
            id='user',
            item_id_getter=lambda x: x[1],
            items='elems',
            on_click=select_status
        ),
            id="elems",
            width=2,
            height=8
        ),
        Button(Const('Вернуться в главное меню'), id='button_start', on_click=dialog_base_def.go_start),
        state=StatusOrder.get_status,
        getter=status_getter
    )
)
