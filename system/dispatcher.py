import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='settings/.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(BOT_TOKEN)

SECRET_KEY = os.getenv('SECRET_KEY')
logger.info(f'SECRET_KEY: {SECRET_KEY}')  # Секретный ключ, для оплаты

ACCOUNT_ID = os.getenv('ACCOUNT_ID')
logger.info(f'ACCOUNT_ID: {ACCOUNT_ID}')  # ID магазина

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
logger.info(f'ADMIN_CHAT_ID: {ADMIN_CHAT_ID}')  # ID магазина

GIGA_CHAT = os.getenv('GIGA_CHAT')
logger.info(f'GIGA_CHAT: {GIGA_CHAT}')  # GIGA_CHAT

GROQ_KEY = os.getenv('GROQ_KEY')
logger.info(f'GROQ_KEY: {GROQ_KEY}')  # GROQ_KEY

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)
