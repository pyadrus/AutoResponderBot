# -*- coding: utf-8 -*-
from datetime import datetime

from loguru import logger
from peewee import SqliteDatabase, IntegerField, TextField, Model, CharField, DateTimeField

# Настройка подключения к базе данных SQLite (или другой базы данных)
db = SqliteDatabase('db/database.db')


class TimeSend(Model):
    user_id = IntegerField(unique=True)
    time_send = TextField()

    class Meta:
        database = db
        table_name = "time_send"


class AIPromt(Model):
    """Промт для ИИ"""
    ai_promt = TextField()

    class Meta:
        database = db
        table_name = "ai_promt"
        primary_key = False  # Для запрета автоматически создающегося поля id (как первичный ключ)


class UserModel(Model):
    """ИИ модель"""
    selected_model = CharField()

    class Meta:
        database = db
        table_name = "usermodel"
        primary_key = False  # Для запрета автоматически создающегося поля id (как первичный ключ)


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

    # Удаляем дубликаты по user_id
    UserWrotePersonalAccount.delete().where(UserWrotePersonalAccount.user_id == user_id).execute()

    # Создаем новую запись
    user_wrote_personal_account = UserWrotePersonalAccount.create(
        user_id=user_id,
        user_bot=user_bot,
        user_first_name=user_first_name or "None",
        user_last_name=user_last_name or "None",
        user_username=user_username or "None",
        user_language_code=user_language_code or "None",
        user_is_premium=user_is_premium or "None",
        user_added_to_attachment_menu=user_added_to_attachment_menu or "None",
        user_can_join_groups=user_can_join_groups or "None",
        user_can_read_all_group_messages=user_can_read_all_group_messages or "None",
        user_supports_inline_queries=user_supports_inline_queries or "None",
        user_can_connect_to_business=user_can_connect_to_business or "None",
        user_has_main_web_app=user_has_main_web_app or "None",
    )
    user_wrote_personal_account.save()


def recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date):
    """Запись данных о пользователей в таблицу, которые запустили бота"""
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
