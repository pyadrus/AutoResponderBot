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

def select_model_keyboard():
    """Клавиатура выбора ИИ модели"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="qwen-qwq-32b", callback_data="qwen-qwq-32b")],
        [InlineKeyboardButton(text="deepseek-r1-distill-llama-70b", callback_data="deepseek-r1-distill-llama-70b"), ],
        [InlineKeyboardButton(text='gemma2-9b-it', callback_data='gemma2-9b-it')],
        [InlineKeyboardButton(text='compound-beta', callback_data='compound-beta')] ,
        [InlineKeyboardButton(text='compound-beta-mini', callback_data='compound-beta-mini'),],
        [InlineKeyboardButton(text='distil-whisper-large-v3-en', callback_data='distil-whisper-large-v3-en'),],
        [InlineKeyboardButton(text='llama-3.1-8b-instant', callback_data='llama-3.1-8b-instant'),],
        [InlineKeyboardButton(text='llama-3.3-70b-versatile', callback_data='llama-3.3-70b-versatile'),],
        [InlineKeyboardButton(text='llama-guard-3-8b', callback_data='llama-guard-3-8b'),],
        [InlineKeyboardButton(text='llama3-70b-8192', callback_data='llama3-70b-8192'),],
        [InlineKeyboardButton(text='llama3-8b-8192', callback_data='llama3-8b-8192'),],
        [InlineKeyboardButton(text='meta-llama/llama-4-maverick-17b-128e-instruct', callback_data='meta-llama/llama-4-maverick-17b-128e-instruct'),],
        [InlineKeyboardButton(text='meta-llama/llama-4-scout-17b-16e-instruct', callback_data='meta-llama/llama-4-scout-17b-16e-instruct'),],
        [InlineKeyboardButton(text='mistral-saba-24b', callback_data='mistral-saba-24b'),],
        [InlineKeyboardButton(text='whisper-large-v3', callback_data='whisper-large-v3'),],
        [InlineKeyboardButton(text='whisper-large-v3-turbo', callback_data='whisper-large-v3-turbo'),],
        [InlineKeyboardButton(text='playai-tts', callback_data='playai-tts'),],
        [InlineKeyboardButton(text='Nasser-PlayAI', callback_data='Nasser-PlayAI'),],
        [InlineKeyboardButton(text='allam-2-7b', callback_data='allam-2-7b'),],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu'), ]
    ])

if __name__ == '__main__':
    greeting_keyboard()
