from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger


def greeting_keyboard():
    """Клавиатура для приветствия"""
    try:
        rows = [
            [InlineKeyboardButton(text='🕒 Изменить время работы', callback_data='change_opening_hours'), ],
            [InlineKeyboardButton(text='👨‍💻 Об авторе', callback_data='about_the_author'),
             InlineKeyboardButton(text='❓ Помощь', callback_data='help')],
        ]
        greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return greeting_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == '__main__':
    greeting_keyboard()
