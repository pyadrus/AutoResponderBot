# -*- coding: utf-8 -*-
import os

from groq import Groq
from loguru import logger

from db.database import UserModel
from proxy.proxy_config import setup_proxy
from utils.dispatcher import GROQ_KEY

user_dialogs = {}  # Словарь для хранения истории диалогов

# Путь к файлу базы знаний
KNOWLEDGE_BASE_PATH = "knowledge_base/data.txt"


# Чтение базы знаний
def load_knowledge_base():
    """Загружает содержимое файла базы знаний."""
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
            return file.read()
    else:
        return "База знаний не найдена. Пожалуйста, создайте файл knowledge_base/data.txt."


async def get_chat_completion(message, system_prompt):
    """Возвращает ответ пользователя"""
    try:
        setup_proxy()  # Установка прокси
        client = Groq(api_key=GROQ_KEY)

        # Считываем с базы данных, ИИ модель выбранную пользователем
        user = UserModel.get_or_none(UserModel.user_id == message.from_user.id)
        logger.info(f"User selected model: {user.selected_model}")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text},
            ],
            model=f"{user.selected_model}",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.exception(e)
