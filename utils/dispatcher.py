# -*- coding: utf-8 -*-
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен бота
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # ID магазина
GROQ_KEY = os.getenv('GROQ_KEY')  # GROQ_KEY
ADMIN_ID = os.getenv("ADMIN_ID")  # ADMIN_ID
USER = os.getenv('USER')  # логин для прокси
PASSWORD = os.getenv('PASSWORD')  # пароль для прокси
PORT = os.getenv('PORT')  # порт для прокси
IP = os.getenv('IP')  # IP для прокси

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)
