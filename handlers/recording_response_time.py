# -*- coding: utf-8 -*-
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from db.database import db, TimeSend
from keyboards.inline import back_to_menu
from states.groups import EnterTime
from utils.dispatcher import bot, router
from utils.file_utils import data


@router.callback_query(F.data == "recording_response_time")
async def time_callback_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Ввод времени для ответа"""
    try:
        await bot.send_message(callback_query.from_user.id, "Введите время для ответа в секундах: ")
        await state.set_state(EnterTime.enter_time)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(EnterTime.enter_time)
async def save_time_handler(message: Message, state: FSMContext) -> None:
    """Сохранение времени для ответа"""
    timeout_seconds = message.text.strip()
    if not timeout_seconds:
        await message.answer("Строка не может быть пустая. Попробуйте снова.")
        return
    await state.update_data(prompt=timeout_seconds)
    data["timeout_seconds"] = timeout_seconds
    db.create_tables([TimeSend], safe=True)
    try:
        with db.atomic():
            TimeSend.insert(user_id=message.from_user.id, time_send=timeout_seconds).on_conflict(
                conflict_target=[TimeSend.user_id], update={TimeSend.time_send: timeout_seconds}).execute()
        await message.answer("Время сохранено успешно!", reply_markup=back_to_menu())
    except Exception as e:
        logger.error(f"Ошибка при сохранении времени: {e}")
        await message.answer("Произошла ошибка при сохранении времени. Попробуйте снова.")
    await state.clear()


def register_time_handlers():
    """Register handlers for the bot."""
    router.callback_query.register(time_callback_handler, F.data == "recording_response_time")
    router.message.register(save_time_handler, EnterTime.enter_time)
