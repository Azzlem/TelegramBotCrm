import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str
    TOKEN: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def db_url(self):
        """ Returns the database URL """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

string_cancel = 'Вы вышли из операции изменения\n\nВыберите в меню новый запрос!\n'
rus_name_status = ["ПРИНЯТ", "НАЗНАЧЕН", "В РАБОТЕ", "ТЕХНИКА В СЦ", "ОПЛАЧЕН", "ВЫДАН КЛИЕНТУ", "ЗАКРЫТ"]
PHOTO_FOLDER_PATH = f'{os.getcwd()}/photo'
