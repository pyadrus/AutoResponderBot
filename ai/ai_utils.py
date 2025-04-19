# -*- coding: utf-8 -*-
import os

from aiogram.types import Message
from gigachat import GigaChat
from groq import Groq

from loguru import logger

from proxy_config import setup_proxy
from utils.dispatcher import GIGA_CHAT, GROQ_KEY


def system_prompt(work):
    """Промт для ИИ"""

    if work == 'Время не рабочее':
        return """Текущее время является нерабочим. Ваш запрос будет рассмотрен позже. Спасибо за понимание! 🕒📅"""
    else:
        return """Сейчас рабочее время. Ваш запрос будет рассмотрен в ближайшее время. 🕐📋"""


async def get_chat_completion_gigachat(message: Message, work):
    """Возвращает ответ пользователя"""

    try:
        # Авторизация в GigaChat
        llm = GigaChat(credentials=GIGA_CHAT, scope="GIGACHAT_API_PERS", model="GigaChat",
                       # Отключает проверку наличия сертификатов НУЦ Минцифры
                       verify_ssl_certs=False,
                       streaming=False, )

        messages = [SystemMessage(content=system_prompt(work)), HumanMessage(content=message.text), ]

        response = llm.invoke(messages)
        print("GigaChat: ", response.content)

        return response.content
    except Exception as e:
        logger.exception(e)


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

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text},
            ],
            model="gemma2-9b-it",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.exception(e)
