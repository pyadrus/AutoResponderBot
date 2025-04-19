import yaml
from loguru import logger

# Считываем файл
with open('messages/messages.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

# Получаем текст
menu_text = data['menu']['text']
logger.info(menu_text)

# Получаем текст
about_author = data['about_author']['text']
logger.info(about_author)
