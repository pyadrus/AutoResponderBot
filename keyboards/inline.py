# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    """Клавиатура для приветствия"""

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🕒 Изменить время работы', callback_data='change_opening_hours'), ],
        [InlineKeyboardButton(text='Получение клиентской базы', callback_data='getting_customer_base'), ],
        [InlineKeyboardButton(text='Настройки', callback_data='settings'), ],
        [InlineKeyboardButton(text='👨‍💻 Об авторе', callback_data='about_the_author'),
         InlineKeyboardButton(text='❓ Помощь', callback_data='help')],
    ])


def back_to_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]], )


def setting_keyboard():
    """Клавиатура для настроек"""

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбор ИИ модели", callback_data="select_model")],
        [InlineKeyboardButton(text="Ввести промт для ИИ модели", callback_data="enter_prompt"), ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]
    ])


if __name__ == '__main__':
    greeting_keyboard()
