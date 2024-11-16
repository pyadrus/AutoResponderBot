from datetime import datetime
from aiogram.types import Message
from groq import Groq

from settings import secrets


def system_prompt(work):
    """Промт для ИИ"""

    return f"""Используй эмодзи в своих ответах. Твоя задача ответить пользователю, что вейчас время {work} и если вреня {work} - не рабочее, 
               то отвечай, что вош вопросс будет расмотвен позже. Если рабочее время, то тапиши, что вопросс, будет расмотрен в ближайшее время."""


async def get_chat_completion(message: Message, work):
    """Возвращает ответ пользователя"""
    
    client = Groq(api_key=secrets.openai_key)

    chat_completion = client.chat.completions.create(

        messages=[
            {"role": "system", "content": system_prompt(work)},
            {"role": "user", "content": message.text},
        ],

        model="llama3-groq-70b-8192-tool-use-preview",
    )

    return chat_completion.choices[0].message.content


async def handle_business_message(message: Message):
    """
   Обрабатывает сообщение от пользователя.

   Args:
       message (Message): Объект сообщения.

   Returns:
       None
   """
    
    # Создаем словарь с рабочим временем
    working_hours = {
        'start': {'hour': 8, 'minute': 0},   # Начало рабочего дня в 09:00
        'end': {'hour': 20, 'minute': 0}     # Окончание рабочего дня в 18:00
    }

    # Получаем текущее время
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Проверяем, находится ли текущее время внутри рабочего интервала
    if (current_hour >= working_hours['start']['hour'] and current_hour <= working_hours['end']['hour']) or \
            (current_hour == working_hours['start']['hour'] and current_minute >= working_hours['start']['minute']) or \
            (current_hour == working_hours['end']['hour'] and current_minute < working_hours['end']['minute']):
        print("Время рабочее.")
        work = "Время рабочее."
    
    else:
        print("Время не рабочее.")
        work = "Время не рабочее."
    
    
    answer = await get_chat_completion(message, work)
    await message.reply(answer)
