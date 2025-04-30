# -*- coding: utf-8 -*-
import os

from groq import Groq
from loguru import logger

from configs.configs import get_proxy_user, get_proxy_password, get_proxy_port, get_proxy_ip
from db.database import UserModel, AIPromt
from utils.dispatcher import GROQ_KEY

user_dialogs = {}  # Словарь для хранения истории диалогов


def setup_proxy():
    # Указываем прокси для HTTP и HTTPS
    os.environ['http_proxy'] = f"http://{get_proxy_user()}:{get_proxy_password()}@{get_proxy_ip()}:{get_proxy_port()}"
    os.environ['https_proxy'] = f"http://{get_proxy_user()}:{get_proxy_password()}@{get_proxy_ip()}:{get_proxy_port()}"


# Чтение базы знаний
def load_knowledge_base():
    """Загружает содержимое файла базы знаний."""
    if os.path.exists("db/data.txt"):
        with open("db/data.txt", "r", encoding="utf-8") as file:
            return file.read()
    else:
        return "База знаний не найдена. Пожалуйста, создайте файл db/data.txt."


async def get_chat_completion(message, knowledge_base_content):
    """Возвращает ответ пользователя"""
    try:
        setup_proxy()  # Установка прокси
        client = Groq(api_key=GROQ_KEY)

        # Считываем с базы данных, ИИ модель выбранную пользователем
        user_record = UserModel.get_or_none()
        user = user_record.selected_model if user_record else ""
        print(user)
        # Считываем промт с базы данных
        system_prompt_record = AIPromt.get_or_none()
        system_prompt = system_prompt_record.ai_promt if system_prompt_record else ""
        print(system_prompt)

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"{system_prompt} {knowledge_base_content}"},
                {"role": "user", "content": f"{message.text}"},
            ],
            model=f"{user}",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.exception(e)
        return None
