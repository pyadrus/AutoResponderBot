from aiogram import Bot
from pydantic_settings import BaseSettings


class Secrets(BaseSettings):
    token: str
    admin_id: int
    openai_key: str
    giga_chat: str

    class Config:
        env_file = "settings/.env"
        env_file_encoding = "utf-8"


secrets = Secrets()

bot = Bot(token=secrets.token)
