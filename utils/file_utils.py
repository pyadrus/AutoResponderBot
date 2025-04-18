import json
import os

from loguru import logger


def save_data_to_json(data, file_path):
    """
    Универсальная функция для сохранения данных в JSON файл.

    :param data: Данные, которые нужно сохранить.
    :param file_path: Путь к файлу JSON, куда будут сохранены данные.
    """
    try:
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Данные успешно сохранены в {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении в JSON файл {file_path}: {e}")


def load_bot_info(messages):
    try:
        with open(messages, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        logger.error(f"Ошибка: {e}")
