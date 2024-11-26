from peewee import *
from loguru import logger

# Модель для таблицы в базе данных
db = SqliteDatabase('db/database.db')


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
