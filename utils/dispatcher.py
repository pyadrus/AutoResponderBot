# -*- coding: utf-8 -*-
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv(dotenv_path='settings/configs.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен бота
SECRET_KEY = os.getenv('SECRET_KEY')  # Секретный ключ, для оплаты
ACCOUNT_ID = os.getenv('ACCOUNT_ID')  # ID магазина
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # ID магазина
GIGA_CHAT = os.getenv('GIGA_CHAT')  # GIGA_CHAT
GROQ_KEY = os.getenv('GROQ_KEY')  # GROQ_KEY

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)
