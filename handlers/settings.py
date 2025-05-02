# -*- coding: utf-8 -*-
from aiogram import F
from aiogram import types

from keyboards.inline import setting_keyboard
from utils.dispatcher import bot, router, ADMIN_ID
from utils.file_utils import data


@router.callback_query(F.data == "settings")
async def settings_handler(callback_query: types.CallbackQuery) -> None:
    """
    Меню настроек Telegram бота
    :param callback_query: Объект CallbackQuery
    :returns: None
    """
    if callback_query.from_user.id != int(ADMIN_ID):
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
