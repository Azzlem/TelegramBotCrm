from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from actions_base.actions_items import ItemsActions
from actions_base.actions_users import UserActions
from keybords.keyboards import keyboard_choise_vendor, keyboard_all_order_from_user
from models.models import Vendor
from permission import is_owner_admin_user
from states.states_items import FormAddItem
from states.states_user import FormChangePermsUser

router = Router()
vendor = Vendor


@router.message(Command(commands=["item_add"]))
async def add_item(message: Message, state: FSMContext):
    user = await UserActions.get_user(message.from_user)
    if await is_owner_admin_user(user):
        keyboard = await keyboard_choise_vendor()
        await message.answer(
            text=f'Выберите вендор',
            reply_markup=keyboard
        )
        await state.set_state(FormAddItem.vendor)
    else:
        await message.answer(text="У вас нет прав!")
        await state.clear()


@router.callback_query(StateFilter(FormAddItem.vendor),
                       F.data.in_([el.name for el in vendor]))
async def add_vendor(callback: CallbackQuery, state: FSMContext):
    await state.update_data(vendor=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        'Введите модель техники'
    )
    await state.set_state(FormAddItem.model)


@router.message(StateFilter(FormAddItem.model))
async def add_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer(
        "Напишите неисправность"
    )
    await state.set_state(FormAddItem.defect)


@router.message(StateFilter(FormAddItem.defect))
async def add_defect(message: Message, state: FSMContext):
    await state.update_data(defect=message.text)
    keyboard = await keyboard_all_order_from_user(message.from_user)
    if not keyboard:
        await message.answer(
            text=f"У вас нет заказов\n"
                 f"Сделайте сначала заказ."
        )
        await state.clear()
    else:
        await message.answer(
            text="Выберите заказ",
            reply_markup=keyboard
        )
        await state.set_state(FormAddItem.order_id)


@router.callback_query(StateFilter(FormAddItem.order_id))
async def add_order_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(order_id=int(callback.data))
    await callback.message.delete()
    data = await state.get_data()
    await ItemsActions.add_item(data)
    await callback.message.answer(
        text="Вы добавили технику к заказу."
    )
    await state.clear()
