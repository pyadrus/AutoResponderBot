from datetime import datetime

from loguru import logger
from peewee import *

# Настройка подключения к базе данных SQLite (или другой базы данных)
db = SqliteDatabase('db/database.db')


# Модель для хранения сообщений пользователей
class UserMessage(Model):
    user_id = IntegerField()
    message_text = TextField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db  # Определяем базу данных, с которой будет работать модель

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
        user_id = IntegerField()
        message_text = TextField()
        timestamp = DateTimeField(default=datetime.now)

        class Meta:
            database = db
            table_name = f"user_{user_id}"

    # Создаем таблицу
    db.create_tables([UserMessageTable], safe=True)

    return UserMessageTable

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
