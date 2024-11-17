from aiogram import Bot
from pydantic_settings import BaseSettings


class Secrets(BaseSettings):
    token: str
    admin_id: int
    openai_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


secrets = Secrets()

bot = Bot(token=secrets.token)
