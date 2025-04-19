# -*- coding: utf-8 -*-
import json
from datetime import datetime

from aiogram.types import Message
from loguru import logger

from ai.ai_utils import get_chat_completion, load_knowledge_base
from db.database import create_user_table, recording_data_users_who_wrote_personal_account
from utils.dispatcher import router, ADMIN_CHAT_ID

# Глобальные словари для хранения состояния пользователей
notified_users = {}
answered_users = {}


# Пример использования
def save_user_message(business_id, user_id, user_first_name, user_last_name, user_username, message_text):
    """
    Сохраняет сообщение в таблице пользователя.
    """
    try:
        # Создаем или получаем таблицу для конкретного пользователя
        UserMessageTable = create_user_table(business_id)
        if not UserMessageTable:
            user_first_name = ''
        if not user_last_name:
            user_last_name = ''
        if not user_username:
            user_username = ''
        # Сохраняем сообщение в таблице
        UserMessageTable.create(business_id=business_id, user_id=user_id, user_first_name=user_first_name,
                                user_last_name=user_last_name, user_username=user_username, message_text=message_text)
        logger.info(f"Сообщение от пользователя {user_id} сохранено в таблице {UserMessageTable._meta.table_name}.")
    except Exception as e:
        logger.info(f"Ошибка при сохранении сообщения: {e}")


@router.business_message()
async def handle_business_message(message: Message):
    """
    Обрабатывает сообщение от пользователя и проверяет рабочее время.
    Если рабочее время, бот отвечает, если нет - не отвечает.
    Также отвечает на запросы, связанные с паролем.
    """
    try:
        message_text_business_connection = message.business_connection_id

        message_text = message.text
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
        recording_data_users_who_wrote_personal_account(**user_data)
        if user_id != int(ADMIN_CHAT_ID):
            save_user_message(message_text_business_connection, user_id, message.from_user.first_name,
                              message.from_user.last_name, message.from_user.username,
                              f"Сообщение от пользователя: {message_text}")
        else:
            save_user_message(message_text_business_connection, user_id, message.from_user.first_name,
                              message.from_user.last_name, message.from_user.username,
                              f"Сообщение от администратора: {message_text}")

        # Загружаем базу знаний при запуске
        knowledge_base_content = load_knowledge_base()

        system_prompt = "Ты - бот, который отвечает на вопросы пользователей."
        ai_response = await get_chat_completion(message, system_prompt)
        await message.reply(f"{ai_response}")

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
            # Если рабочее время, очищаем информацию об уведомленных пользователях
            if user_id in notified_users:
                del notified_users[user_id]

            # Проверяем, отвечал ли бот уже пользователю в рабочее время
            if user_id not in answered_users:
                if message.from_user.id not in [int(ADMIN_CHAT_ID)]:
                    await message.reply(
                        "✅ **Сейчас рабочее время!**\n\n"
                        "Здравствуйте!"
                        , parse_mode="Markdown")
                    # Сохраняем состояние пользователя, чтобы не отвечать повторно
                    answered_users[user_id] = True
        else:
            # Проверяем, уведомляли ли мы пользователя ранее в нерабочее время
            if user_id not in notified_users:
                if message.from_user.id not in [int(ADMIN_CHAT_ID)]:
                    await message.reply(
                        "❌ **Сейчас нерабочее время!**\n\n"
                        "Здравствуйте!\n"
                        , parse_mode="Markdown")
                    # Сохраняем состояние пользователя для нерабочего времени
                    notified_users[user_id] = True

            # Очищаем состояние для рабочего времени, чтобы бот снова мог ответить в рабочее время
            if user_id in answered_users:
                del answered_users[user_id]
    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")


def register_handle_business_message():
    router.business_message.register(handle_business_message)


if __name__ == "__main__":
    register_handle_business_message()
