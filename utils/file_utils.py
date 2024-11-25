import json
from loguru import logger

def save_user_data_to_json(user_id, data):
    """Запись данных в json файл"""
    file_path = f"data/{user_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# def save_user_data_to_json(user_id, data):
#     """Запись данных в json файл"""
#     file_path = f"data/{user_id}.json"
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

def load_bot_info(messages):
    try:
        with open(messages, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def save_bot_info(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


# Функция для сохранения данных в JSON файл
def save_to_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Ошибка при сохранении в JSON: {e}")
