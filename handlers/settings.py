# -*- coding: utf-8 -*-
from aiogram import F
from aiogram import types
from loguru import logger

from configs.configs import get_telegram_admin_id
from keyboards.inline import setting_keyboard
from utils.dispatcher import bot, router
from utils.file_utils import data


@router.callback_query(F.data == "settings")
async def settings_handler(callback_query: types.CallbackQuery) -> None:
    """
    Меню настроек Telegram бота
    :param callback_query: Объект CallbackQuery
    :returns: None
    """
    if callback_query.from_user.id != int(get_telegram_admin_id()): # Преобразование в int, чтобы сравнивать с id пользователя
        await callback_query.answer("У вас нет прав для выполнения этой команды!", show_alert=True)
        return

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=data['menu']['text'],
        reply_markup=setting_keyboard(),
        parse_mode="HTML"
    )


def register_settings_handler():
    """Регистрация обработчиков для бота"""
    router.message.register(register_settings_handler)
