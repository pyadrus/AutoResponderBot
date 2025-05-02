# -*- coding: utf-8 -*-
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from keyboards.inline import back_to_menu
from states.groups import EnterPrompt, EnterKnowledge
from utils.dispatcher import bot, router


@router.callback_query(F.data == "replacing_knowledge_base")
async def replacing_knowledge_base_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle callback query to prompt user for AI prompt input."""
    try:
        await bot.send_message(callback_query.from_user.id, "Пришлите базу знаний для ии в формате data.txt")
        await state.set_state(EnterKnowledge.enter_knowledge)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


# Обработчик приема документа
@router.message(EnterKnowledge.enter_knowledge, F.document)
async def save_replacing_knowledge_base(message: Message, state: FSMContext) -> None:
    """Обрабатываем получение файла и сохранение его локально"""
    try:
        # Проверяем название файла
        if not message.document.file_name.endswith(".txt"):
            await message.answer("Имя файла должно заканчиваться на .txt")
            return

        # Загружаем файл
        file = await bot.get_file(message.document.file_id)

        # Скачиваем файл
        await bot.download_file(file.file_path,
                                destination=f"db/{message.document.file_name}")  # Полный путь для сохранения файла

        await message.answer("Файл успешно загружен!", reply_markup=back_to_menu())
    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await message.answer("Произошла ошибка при сохранении файла. Попробуйте снова.")

    await state.clear()


def register_replacing_knowledge_base_handlers():
    """Register handlers for the bot."""
    router.callback_query.register(replacing_knowledge_base_handler, F.data == "replacing_knowledge_base")
    router.message.register(save_replacing_knowledge_base, EnterPrompt.enter_prompt)
