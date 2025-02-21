from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger


def greeting_keyboard():
    """Клавиатура для приветствия"""
    try:
        rows = [
            [InlineKeyboardButton(text='🕒 Изменить время работы', callback_data='change_opening_hours'), ],
            [InlineKeyboardButton(text='Получение клиентской базы', callback_data='getting_customer_base'),],
            [InlineKeyboardButton(text='👨‍💻 Об авторе', callback_data='about_the_author'),
             InlineKeyboardButton(text='❓ Помощь', callback_data='help')],
        ]
        greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return greeting_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def back_to_menu():
    try:
        rows = [
            [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ],
        ]
        back_to_menu = InlineKeyboardMarkup(inline_keyboard=rows)
        return back_to_menu
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == '__main__':
    greeting_keyboard()
