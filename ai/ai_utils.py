from aiogram.types import Message
from gigachat import GigaChat
from groq import Groq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
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
