# -*- coding: utf-8 -*-
from datetime import datetime

from loguru import logger
from peewee import *

# Настройка подключения к базе данных SQLite (или другой базы данных)
db = SqliteDatabase('db/database.db')

class UserModel(Model):
    user_id = IntegerField(unique=True)
    selected_model = CharField()

    class Meta:
        database = db

# Инициализация базы данных
db.connect()
db.create_tables([UserModel], safe=True)

class UserWrotePersonalAccount(Model):
    user_id = CharField()
    user_bot = CharField()
    user_first_name = CharField()
    user_last_name = CharField()
    user_username = CharField()
    user_language_code = CharField()
    user_is_premium = CharField()
    user_added_to_attachment_menu = CharField()
    user_can_join_groups = CharField()
    user_can_read_all_group_messages = CharField()
    user_supports_inline_queries = CharField()
    user_can_connect_to_business = CharField()
    user_has_main_web_app = CharField()

    class Meta:
        database = db
        table_name = "user_wrote_personal_account"


# Модель для хранения сообщений пользователей
# class UserMessage(Model):
#     user_id = IntegerField()
#     message_text = TextField()
#     timestamp = DateTimeField(default=datetime.now)
#
#     class Meta:
#         database = db  # Определяем базу данных, с которой будет работать модель


class UserStart(Model):
    try:
        telegram_id = CharField()  # Идентификатор пользователя Telegram
        telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
        user_first_name = CharField()  # Имя пользователя
        user_last_name = CharField()  # Фамилия пользователя
        user_date = CharField()  # Дата

        class Meta:
            database = db
    except Exception as e:
        logger.error(f"Ошибка: {e}")


# Функция для создания таблицы для конкретного пользователя
def create_user_table(user_id: int):
    """
    Создает таблицу с именем пользователя (user_id), если она не существует.
    """

    # Динамическое создание таблицы для каждого пользователя

    class UserMessageTable(Model):
        business_id = CharField()  # Идентификатор бизнеса
        user_id = IntegerField()
        user_first_name = CharField()  # Имя пользователя
        user_last_name = CharField()  # Фамилия пользователя
        user_username = CharField()  # Username пользователя
        message_text = TextField()
        timestamp = DateTimeField(default=datetime.now)

        class Meta:
            database = db
            table_name = f"user_{user_id}"

    # Создаем таблицу
    db.create_tables([UserMessageTable], safe=True)

    return UserMessageTable


class UserWrotePersonalAccount(Model):
    try:
        user_id = CharField()
        user_bot = CharField()
        user_first_name = CharField()
        user_last_name = CharField()
        user_username = CharField()
        user_language_code = CharField()
        user_is_premium = CharField()
        user_added_to_attachment_menu = CharField()
        user_can_join_groups = CharField()
        user_can_read_all_group_messages = CharField()
        user_supports_inline_queries = CharField()
        user_can_connect_to_business = CharField()
        user_has_main_web_app = CharField()

        class Meta:
            database = db
            table_name = "user_wrote_personal_account"
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def recording_data_users_who_wrote_personal_account(user_id, user_bot, user_first_name, user_last_name,
                                                    user_username, user_language_code, user_is_premium,
                                                    user_added_to_attachment_menu, user_can_join_groups,
                                                    user_can_read_all_group_messages, user_supports_inline_queries,
                                                    user_can_connect_to_business, user_has_main_web_app):
    """Запись данных о пользователях в таблицу, которые писали в личку"""
    # Создание таблицы, если она еще не создана
    db.create_tables([UserWrotePersonalAccount], safe=True)

    # Обработка значений None
    if user_first_name is None:
        user_first_name = "None"
    if user_last_name is None:
        user_last_name = "None"
    if user_username is None:
        user_username = "None"
    if user_language_code is None:
        user_language_code = "None"
    if user_is_premium is None:
        user_is_premium = "None"
    if user_added_to_attachment_menu is None:
        user_added_to_attachment_menu = "None"
    if user_can_join_groups is None:
        user_can_join_groups = "None"
    if user_can_read_all_group_messages is None:
        user_can_read_all_group_messages = "None"
    if user_supports_inline_queries is None:
        user_supports_inline_queries = "None"
    if user_can_connect_to_business is None:
        user_can_connect_to_business = "None"
    if user_has_main_web_app is None:
        user_has_main_web_app = "None"

    # Удаляем дубликаты по user_id
    UserWrotePersonalAccount.delete().where(UserWrotePersonalAccount.user_id == user_id).execute()

    # Создаем новую запись
    user_wrote_personal_account = UserWrotePersonalAccount.create(
        user_id=user_id,
        user_bot=user_bot,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_username=user_username,
        user_language_code=user_language_code,
        user_is_premium=user_is_premium,
        user_added_to_attachment_menu=user_added_to_attachment_menu,
        user_can_join_groups=user_can_join_groups,
        user_can_read_all_group_messages=user_can_read_all_group_messages,
        user_supports_inline_queries=user_supports_inline_queries,
        user_can_connect_to_business=user_can_connect_to_business,
        user_has_main_web_app=user_has_main_web_app,
    )
    user_wrote_personal_account.save()


def recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date):
    try:
        # Создание таблицы, если она еще не создана
        db.create_tables([UserStart], safe=True)

        # Создание записи в таблице
        user_start = UserStart.create(
            telegram_id=user_id,
            telegram_username=user_name,
            user_first_name=user_first_name,
            user_last_name=user_last_name,
            user_date=user_date,
        )
        user_start.save()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
