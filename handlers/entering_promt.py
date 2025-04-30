# -*- coding: utf-8 -*-
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from db.database import db, AIPromt
from keyboards.inline import back_to_menu
from states.groups import EnterPrompt
from utils.dispatcher import bot, router
from utils.file_utils import data


@router.callback_query(F.data == "enter_prompt")
async def prompt_callback_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle callback query to prompt user for AI prompt input."""
    try:
        await bot.send_message(callback_query.from_user.id, "Введите промт для ИИ")
        await state.set_state(EnterPrompt.enter_prompt)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(EnterPrompt.enter_prompt)
async def save_prompt_handler(message: Message, state: FSMContext) -> None:
    """Handle user input for AI prompt and save it to the database."""
    prompt = message.text.strip()
    if not prompt:
        await message.answer("Промт не может быть пустым. Попробуйте снова.")
        return

    await state.update_data(prompt=prompt)
    data["prompt"] = prompt

    # Создаем таблицу, если она не создана ранее
    db.create_tables([AIPromt], safe=True)

    try:
        with db.atomic():
            # Удаляем все старые записи (если их несколько)
            AIPromt.delete().execute()
            # Вставляем новую
            AIPromt.insert(ai_promt=prompt).execute()

        await message.answer("Промт сохранен!", reply_markup=back_to_menu())
    except Exception as e:
        logger.error(f"Ошибка при сохранении промта: {e}")
        await message.answer("Произошла ошибка при сохранении промта. Попробуйте снова.")

    await state.clear()


def register_prompt_handlers():
    """Register handlers for the bot."""
    router.callback_query.register(prompt_callback_handler, F.data == "enter_prompt")
    router.message.register(save_prompt_handler, EnterPrompt.enter_prompt)
