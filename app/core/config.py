from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


# Старый вариант, который через модуль os получить данные из .env файла в переменную, либо установит дефолт значение
# import os
# DB_HOST = os.getenv('DB_HOST', 'localhost')
# DB_HOST = os.getenv('DB_PORT', '5555')

# Новомодный способ, с помощью BaseSettings из pydantic
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    JWT_ALGORITHM: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # ЗАДЕЛ на валидацию данных в конфиге ПОЧЕКАТЬ КОММЕНТ ПОД УРОКОМ 1.5 шаг 10
        # return PostgresDsn.build(scheme='postgresql+asyncpg',
        #                          username=self.DB_USER,
        #                          password=self.DB_PASS,
        #                          host=str(self.DB_HOST),
        #                          port=self.DB_PORT,
        #                          path=f"/{self.DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
# print(settings.DATABASE_URL)
