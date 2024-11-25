from datetime import datetime
import json
from aiogram.types import Message
from loguru import logger

from utils.dispatcher import router
from utils.file_utils import save_data_to_json


@router.business_message()
async def handle_business_message(message: Message):
    """
    Обрабатывает сообщение от пользователя и проверяет рабочее время.
    Если рабочее время, бот отвечает, если нет - не отвечает.
    """
    try:
        user_id = message.from_user.id
        user_data = {
            "user_id": user_id,
            "user_bot": message.from_user.is_bot,
            "user_first_name": message.from_user.first_name,
            "user_last_name": message.from_user.last_name,
            "user_username": message.from_user.username,
            "user_language_code": message.from_user.language_code,
            "user_is_premium": message.from_user.is_premium,
            "user_added_to_attachment_menu": message.from_user.added_to_attachment_menu,
            "user_can_join_groups": message.from_user.can_join_groups,
            "user_can_read_all_group_messages": message.from_user.can_read_all_group_messages,
            "user_supports_inline_queries": message.from_user.supports_inline_queries,
            "user_can_connect_to_business": message.from_user.can_connect_to_business,
            "user_has_main_web_app": message.from_user.has_main_web_app
        }

        # Логируем данные пользователя
        logger.info(f"Пользователь ID: {user_id}. Username: {message.from_user.username}, "
                    f"Фамилия: {message.from_user.last_name}, Имя: {message.from_user.first_name} написал сообщение.")

        file_path = f"data/{user_id}.json"

        # Сохраняем данные пользователя в JSON
        save_data_to_json(data=user_data, file_path=file_path)

        logger.info(f"Данные пользователя: {user_data} записаны или обновлены")

        # Открываем файл и читаем данные рабочего времени
        with open('messages/working_hours.json', 'r') as file:
            data = json.load(file)

        # Получаем данные о начале и конце рабочего времени
        start_hour = int(data['start']['hour'])
        start_minute = int(data['start']['minute'])
        end_hour = int(data['end']['hour'])
        end_minute = int(data['end']['minute'])

        # Получаем текущее время
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute

        # Проверяем, является ли текущее время рабочим
        is_working_time = (
                (start_hour < current_hour < end_hour) or
                (current_hour == start_hour and current_minute >= start_minute) or
                (current_hour == end_hour and current_minute < end_minute)
        )

        if is_working_time:
            await message.reply("Сейчас рабочее время.\n\nВаш запрос будет рассмотрен в ближайшее время. 🕐📋")
        else:
            await message.reply(
                "Текущее время является нерабочим.\n\nВаш запрос будет рассмотрен позже. Спасибо за понимание! 🕒📅")
    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")


def register_handle_business_message():
    router.business_message.register(handle_business_message)


if __name__ == "__main__":
    register_handle_business_message()
