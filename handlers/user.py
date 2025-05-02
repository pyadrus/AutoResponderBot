# -*- coding: utf-8 -*-
from aiogram import F, types
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from db.database import recording_user_data_of_the_launched_bot
from keyboards.inline import greeting_keyboard
from utils.dispatcher import bot, router
from utils.file_utils import data


@router.message(Command("start"))
async def user_start_handler(message: Message) -> None:
    """Обработчик команды /start. Главное меню бота"""
    try:
        recording_user_data_of_the_launched_bot(message.from_user.id, message.from_user.username or '',
                                                message.from_user.first_name, message.from_user.last_name or '',
                                                message.date.strftime("%Y-%m-%d %H:%M:%S"))
        await bot.send_message(
            chat_id=message.from_user.id,
            text=data['menu']['text'],
            reply_markup=greeting_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.callback_query(F.data == "back_to_menu")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    """Обработчик кнопки "Назад в главное меню" """
    try:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=data['menu']['text'],
            reply_markup=greeting_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def register_greeting_user_handler():
    """Регистрация обработчиков для бота"""
    router.message.register(user_start_handler)
    router.message.register(instructions_handlers)  # обработчик для кнопки "Назад"
