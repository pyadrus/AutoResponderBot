# -*- coding: utf-8 -*-
import asyncio

from aiogram.types import Message
from loguru import logger

from ai.ai_utils import get_chat_completion, load_knowledge_base
from db.database import recording_data_users_who_wrote_personal_account, save_user_message
from utils.dispatcher import router, ADMIN_CHAT_ID

# Глобальные словари для хранения состояния пользователей
# notified_users = {}
# answered_users = {}


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
            save_user_message(
                message_text_business_connection,
                user_id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
                f"Сообщение от пользователя: {message_text}"
            )
        else:
            save_user_message(message_text_business_connection, user_id, message.from_user.first_name,
                              message.from_user.last_name, message.from_user.username,
                              f"Сообщение от администратора: {message_text}")

        knowledge_base_content = load_knowledge_base()  # Загружаем базу знаний при запуске
        ai_response = await get_chat_completion(message, knowledge_base_content)

        await asyncio.sleep(int(2))
        await message.reply(f"{ai_response}")

    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")


def register_handle_business_message():
    router.business_message.register(handle_business_message)


if __name__ == "__main__":
    register_handle_business_message()
