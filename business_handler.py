import asyncio

from aiogram.types import Message
from groq import Groq

from settings import secrets

def system_prompt():
    return """Ты бот помощник и ты должен помогать людям. Если тебе написали в не рабочее время, то ты должен ответить, что я отвечу позже"""

async def get_chat_completion(message: Message):
    client = Groq(api_key=secrets.openai_key)

    chat_completion = client.chat.completions.create(

        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": message.text},
        ],

        model="llama3-groq-70b-8192-tool-use-preview",
    )

    return chat_completion.choices[0].message.content


# Используем словарь для хранения времени последнего сообщения пользователя
last_message_times = {}


async def check_user_delay(user_id: int):
    current_time = asyncio.get_event_loop().time()

    # Проверяем, если для пользователя есть сохраненное время последнего сообщения
    if user_id in last_message_times:
        time_since_last_message = current_time - last_message_times[user_id]
        if time_since_last_message < secrets.delay * 60:
            return False

    # Обновляем время последнего сообщения
    last_message_times[user_id] = current_time
    return True


async def handle_business_message(message: Message):
    if await check_user_delay(message.from_user.id) and message.text:
        answer = await get_chat_completion(message)
        await message.reply(answer)
