# -*- coding: utf-8 -*-
from aiogram import F
from aiogram import types
from loguru import logger

from keyboards.inline import back_to_menu
from messages.messages import data
from utils.dispatcher import bot, router


@router.callback_query(F.data == "settings")
async def settings_handler(callback_query: types.CallbackQuery) -> None:
    """Настройки"""
    try:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=data['menu']['text'],
                               reply_markup=back_to_menu(),
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def register_settings_handler():
    """Регистрация обработчиков для бота"""
    router.message.register(register_settings_handler)
