from datetime import datetime
import json
from aiogram.types import Message

from loguru import logger


def save_user_data_to_json(user_id, data):
    """Запись данных в json файл"""
    file_path = f"{user_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def handle_business_message(message: Message):
    """
    Обрабатывает сообщение от пользователя. И проверяет рабочее время или нет. Если рабочее время, то бот отвечает пользователю,
    Если время не рабочее, то не отвечает.
    """

    user_id = message.from_user.id
    user_bot = message.from_user.is_bot
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    user_language_code = message.from_user.language_code
    user_is_premium = message.from_user.is_premium
    user_added_to_attachment_menu = message.from_user.added_to_attachment_menu
    user_can_join_groups = message.from_user.can_join_groups
    user_can_read_all_group_messages = message.from_user.can_read_all_group_messages
    user_supports_inline_queries = message.from_user.supports_inline_queries
    user_can_connect_to_business = message.from_user.can_connect_to_business
    user_has_main_web_app = message.from_user.has_main_web_app

    logger.info(
        f"Пользователь ID: {user_id}. Username {user_username}, Фамилия: {user_last_name}, Имя: {user_first_name} написал сообщение.")

    user_data = {
        "user_id": user_id,
        "user_bot": user_bot,
        "user_first_name": user_first_name,
        "user_last_name": user_last_name,
        "user_username": user_username,
        "user_language_code": user_language_code,
        "user_is_premium": user_is_premium,
        "user_added_to_attachment_menu": user_added_to_attachment_menu,
        "user_can_join_groups": user_can_join_groups,
        "user_can_read_all_group_messages": user_can_read_all_group_messages,
        "user_supports_inline_queries": user_supports_inline_queries,
        "user_can_connect_to_business": user_can_connect_to_business,
        "user_has_main_web_app": user_has_main_web_app
    }

    save_user_data_to_json(user_id, user_data)

    logger.info(f"Данные пользователя: {user_data} записаны или обновлены")

    # Создаем словарь с рабочим временем
    working_hours = {
        "start": {"hour": 9, "minute": 0},  # Начало рабочего дня в 09:00
        "end": {"hour": 18, "minute": 0},  # Окончание рабочего дня в 18:00
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
        await message.reply(
            "Текущее время является нерабочим.\n\nВаш запрос будет рассмотрен позже. Спасибо за понимание! 🕒📅")
