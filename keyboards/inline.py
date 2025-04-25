# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    """Клавиатура для приветствия"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Получение клиентской базы', callback_data='getting_customer_base'), ],
        [InlineKeyboardButton(text='Настройки', callback_data='settings'), ],
    ])


def back_to_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]], )


def setting_keyboard():
    """Клавиатура для настроек"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбор ИИ модели", callback_data="select_model")],
        [InlineKeyboardButton(text="Ввести промт для ИИ модели", callback_data="enter_prompt"), ],
        [InlineKeyboardButton(text="Замена базы знаний", callback_data="replacing_knowledge_base"), ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]
    ])


def select_model_keyboard():
    """Клавиатура выбора ИИ модели"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='gemma2-9b-it', callback_data='gemma2-9b-it')],
        [InlineKeyboardButton(text='compound-beta', callback_data='compound-beta')],
        [InlineKeyboardButton(text='compound-beta-mini', callback_data='compound-beta-mini'), ],
        [InlineKeyboardButton(text='llama-3.1-8b-instant', callback_data='llama-3.1-8b-instant'), ],
        [InlineKeyboardButton(text='llama-3.3-70b-versatile', callback_data='llama-3.3-70b-versatile'), ],
        [InlineKeyboardButton(text='llama3-70b-8192', callback_data='llama3-70b-8192'), ],
        [InlineKeyboardButton(text='llama3-8b-8192', callback_data='llama3-8b-8192'), ],
        [InlineKeyboardButton(text='meta-llama/llama-4-maverick-17b-128e-instruct',
                              callback_data='meta-llama/llama-4-maverick-17b-128e-instruct'), ],
        [InlineKeyboardButton(text='meta-llama/llama-4-scout-17b-16e-instruct',
                              callback_data='meta-llama/llama-4-scout-17b-16e-instruct'), ],
        [InlineKeyboardButton(text='allam-2-7b', callback_data='allam-2-7b'), ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]
    ])


if __name__ == '__main__':
    greeting_keyboard()
    back_to_menu()
    setting_keyboard()
    select_model_keyboard()
