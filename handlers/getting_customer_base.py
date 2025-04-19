# -*- coding: utf-8 -*-
import os

from aiogram import F
from aiogram import types
from aiogram.types import FSInputFile
from loguru import logger
from openpyxl.workbook import Workbook

from db.database import UserWrotePersonalAccount
from keyboards.inline import back_to_menu
from utils.dispatcher import bot, router


def export_to_excel():
    """Выгружает данные из БД в Excel"""
    try:
        users = UserWrotePersonalAccount.select()
        if not users.exists():
            return None  # Если данных нет, возвращаем None

        wb = Workbook()
        ws = wb.active
        ws.title = "Клиентская база"

        # Заголовки
        headers = [
            "user_id", "user_bot", "user_first_name", "user_last_name", "user_username",
            "user_language_code", "user_is_premium", "user_added_to_attachment_menu",
            "user_can_join_groups", "user_can_read_all_group_messages",
            "user_supports_inline_queries", "user_can_connect_to_business", "user_has_main_web_app"
        ]
        ws.append(headers)

        # Запись данных
        for user in users:
            ws.append([
                user.user_id, user.user_bot, user.user_first_name, user.user_last_name,
                user.user_username, user.user_language_code, user.user_is_premium,
                user.user_added_to_attachment_menu, user.user_can_join_groups,
                user.user_can_read_all_group_messages, user.user_supports_inline_queries,
                user.user_can_connect_to_business, user.user_has_main_web_app
            ])

        file_path = "customer_base.xlsx"
        wb.save(file_path)
        return file_path  # Возвращаем путь к файлу

    except Exception as e:
        logger.error(f"Ошибка при экспорте в Excel: {e}")
        return None


@router.callback_query(F.data == "getting_customer_base")
async def getting_customer_base_handler(callback_query: types.CallbackQuery) -> None:
    """Получение клиентской базы"""
    try:
        await bot.send_document(callback_query.from_user.id, document=FSInputFile(export_to_excel()),
                                caption="Ваша клиентская база", reply_markup=back_to_menu(),
                                parse_mode="HTML")  # Отправка файла пользователю
        os.remove(export_to_excel())  # Удаление файла
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def register_getting_customer_base_handler():
    """Регистрация обработчиков для бота"""

    router.message.register(getting_customer_base_handler)


if __name__ == "__main__":
    register_getting_customer_base_handler()
