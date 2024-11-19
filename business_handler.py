from datetime import datetime

from aiogram.types import Message

from loguru import logger

async def handle_business_message(message: Message):
    """
    Обрабатывает сообщение от пользователя. И проверяет рабочее время или нет. Если рабочее время, то бот отвечает пользователю,
    Если время не рабочее, то не отвечает.
    """
    id_user = message.from_user.id
    user_name = message.from_user.username

    logger.info(f"Пользователь ID: {id_user}. Username {user_name} написал сообщение.")

    # Создаем словарь с рабочим временем
    working_hours = {
        "start": {"hour": 9, "minute": 0},  # Начало рабочего дня в 09:00
        "end": {"hour": 18, "minute": 0},   # Окончание рабочего дня в 18:00
    }

    # Получаем текущее время
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Проверяем, находится ли текущее время внутри рабочего интервала
    if (
            (
                working_hours["start"]["hour"] <= current_hour < working_hours["end"]["hour"]
            ) or (
                current_hour == working_hours["start"]["hour"]
                and current_minute >= working_hours["start"]["minute"]
            ) or (
                current_hour == working_hours["end"]["hour"]
                and current_minute < working_hours["end"]["minute"]
            )
    ):
        await message.reply("Сейчас рабочее время.\n\nВаш запрос будет рассмотрен в ближайшее время. 🕐📋")
    else:
        await message.reply("Текущее время является нерабочим.\n\nВаш запрос будет рассмотрен позже. Спасибо за понимание! 🕒📅")
