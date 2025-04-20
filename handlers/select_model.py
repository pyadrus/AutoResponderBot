# -*- coding: utf-8 -*-
from aiogram import F
from aiogram import types
from loguru import logger

from db.database import db, UserModel
from keyboards.inline import select_model_keyboard
from utils.dispatcher import bot, router
from utils.file_utils import data


@router.callback_query(F.data == "select_model")
async def select_model_handler(callback_query: types.CallbackQuery) -> None:
    """Настройки выбор моделей"""
    try:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=data['model_selection']['text'],
                               reply_markup=select_model_keyboard(),
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.callback_query(lambda c: c.data in [
    "gemma2-9b-it",
    "compound-beta",
    "compound-beta-mini",
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "allam-2-7b"
])
async def model_selection_handler(callback_query: types.CallbackQuery) -> None:
    """Обработка выбора модели"""
    try:
        user_id = callback_query.from_user.id
        selected_model = callback_query.data

        # Обновление или создание записи в базе данных
        with db.atomic():
            UserModel.insert(
                user_id=user_id,
                selected_model=selected_model
            ).on_conflict(
                conflict_target=[UserModel.user_id],
                update={UserModel.selected_model: selected_model}
            ).execute()

        await callback_query.message.answer(
            f"Выбрана модель: {selected_model}",
            parse_mode="HTML"
        )

        # Опционально: можно вернуться к главному меню
        await callback_query.message.edit_reply_markup(reply_markup=None)

    except Exception as e:
        logger.error(f"Ошибка при выборе модели: {e}")
        await callback_query.message.answer(
            "Произошла ошибка при выборе модели. Попробуйте снова.",
            parse_mode="HTML"
        )


def register_select_model_handler():
    """Регистрация обработчиков для бота"""
    router.message.register(select_model_handler)
