import os

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
