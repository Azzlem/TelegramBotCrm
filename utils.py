import os

from loguru import logger

from actions_base.actions_customers import CustomerActions
from actions_base.actions_items import ItemsActions
from actions_base.actions_orders import OrdersActions
from dataclass import DataClass
from models.models import Customers, Orders, Items
from settings import PHOTO_FOLDER_PATH


async def dowmload_image(message, bot):
    # Получаем объект фото
    photo = message.photo[-1]  # Берем самое последнее фото
    # Получаем идентификатор файла фото
    file_id = photo.file_id
    # Получаем информацию о файле фото
    file_info = await bot.get_file(file_id)
    # Получаем путь для сохранения фото
    photo_path = os.path.join(PHOTO_FOLDER_PATH, f'{file_id}.jpg')
    # Скачиваем фото по ссылке
    await bot.download_file(file_info.file_path, photo_path)
    # Выводим сообщение об успешном сохранении
    await message.answer(f'Фото успешно сохранено!')
    return f'{file_id}.jpg'


class CreateOrderFull:

    @staticmethod
    async def create_customer(**data):
        data_customer = DataClass(data.get('data'))
        try:
            if data.get('customer') is None:
                customer = Customers(
                    fullname=data_customer.name,
                    phone=int(data_customer.phone),
                    address=data_customer.address
                )
                customer = await CustomerActions.custom_add_customer(customer)
                return customer
            else:
                return data['customer']
        except:
            logger.add("logs/file_{time}.json", rotation="weekly")
            logger.exception("What?!")

    @staticmethod
    async def create_order(**data):
        data_order = DataClass(data['data'])
        customer = data['customer']
        try:
            order = await OrdersActions.create_order(customer.id, int(data_order.user))
            return order
        except:
            logger.add("logs/file_{time}.json", rotation="weekly")
            logger.exception("What?!")

    @staticmethod
    def create_item(**data):
        data_item = DataClass(data['data'])
        order_id = data['order_id']
        try:
            item = ItemsActions.add_item(
                {
                    "vendor": data_item.vendor,
                    "model": data_item.model,
                    "defect": data_item.defect,
                    "order_id": int(order_id)
                }
            )
            return item
        except:
            logger.add("logs/file_{time}.json", rotation="weekly")
            logger.exception("What?!")



