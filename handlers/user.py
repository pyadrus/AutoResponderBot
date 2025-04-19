# -*- coding: utf-8 -*-
from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from db.database import recording_user_data_of_the_launched_bot
from keyboards.inline import greeting_keyboard, back_to_menu
from states.groups import FormeditMainMenu, SettingsClass
from utils.dispatcher import bot, ADMIN_CHAT_ID, router
from utils.file_utils import load_bot_info, save_data_to_json

# ADMIN_CHAT_ID должен быть списком строк, а не чисел
ADMIN_CHAT_ID = ["535185511"]

# Путь к JSON файлу, где будут храниться рабочие часы
WORKING_HOURS_FILE = 'messages/working_hours.json'


@router.message(Command("start"))
async def user_start_handler(message: Message) -> None:
    """Обработчик команды /start. Главное меню бота"""
    try:
        user_id = message.from_user.id

        user_name = message.from_user.username
        if message.from_user.username is None:
            user_name = ''  # Установим пустую строку вместо None

        user_first_name = message.from_user.first_name

        user_last_name = message.from_user.last_name
        if message.from_user.last_name is None:
            user_last_name = ''

        user_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name} {user_date}")
        recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date)
        await bot.send_message(message.from_user.id,
                               load_bot_info(messages="messages/main_menu.json"),
                               reply_markup=greeting_keyboard(),
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.callback_query(F.data == "back_to_menu")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    """Обработчик кнопки "Назад в главное меню" """
    try:
        user_id = callback_query.from_user.id

        user_name = callback_query.from_user.username
        if callback_query.from_user.username is None:
            user_name = ''  # Установим пустую строку вместо None

        user_first_name = callback_query.from_user.first_name

        user_last_name = callback_query.from_user.last_name
        if callback_query.from_user.last_name is None:
            user_last_name = ''

        logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
        await bot.send_message(callback_query.from_user.id,
                               load_bot_info(messages="messages/main_menu.json"),
                               reply_markup=greeting_keyboard(),
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(Command("edit_main_menu"))
async def edit_main_menu(message: Message, state: FSMContext):
    """Обработчик команды /edit_main_menu (только для админа) Изменяет текст в главном меню бота"""
    try:
        if message.from_user.id not in ADMIN_CHAT_ID:
            await message.reply("У вас нет прав на выполнение этой команды.")
            return
        await message.answer("Введите новый текст, используя разметку HTML.")
        await state.set_state(FormeditMainMenu.text_edit_main_menu)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(FormeditMainMenu.text_edit_main_menu)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    try:
        text = message.html_text
        bot_info = text
        save_data_to_json(bot_info, file_path='messages/main_menu.json')  # Сохраняем информацию в JSON
        await message.reply("Информация обновлена.")
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(Command("change_opening_hours"))
# @router.callback_query(F.data == "change_opening_hours")
async def start_setting_hours(message: Message, state: FSMContext):
    """Начало ввода рабочего времени"""
    try:
        if str(message.from_user.id) not in ADMIN_CHAT_ID:
            await bot.send_message(message.from_user.id, "У вас нет прав на выполнение этой команды.")
            return
        await bot.send_message(message.from_user.id, text="Введите час начала рабочего дня (0-23):")
        await state.set_state(SettingsClass.setting_start_hour)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(SettingsClass.setting_start_hour)
async def set_start_hour(message: Message, state: FSMContext):
    """Сохранение часа начала рабочего дня"""
    logger.debug("Получено сообщение: %s", message.text)
    start_hour = message.text
    print(start_hour)
    await state.update_data(setting_start_hour=start_hour)
    await message.reply("Введите минуты начала рабочего дня (0-59):")
    await state.set_state(SettingsClass.setting_start_minute)
    logger.info("Состояние установлено на setting_start_minute")


@router.message(SettingsClass.setting_start_minute)
async def set_start_minute(message: Message, state: FSMContext):
    """Сохранение минут начала рабочего дня"""
    try:
        start_minute = int(message.text)
        if not (0 <= start_minute <= 59):
            raise ValueError("Минуты должны быть в диапазоне от 0 до 59.")
        await state.update_data(setting_start_minute=start_minute)
        await message.reply("Введите час окончания рабочего дня (0-23):")
        await state.set_state(SettingsClass.setting_end_hour)
    except ValueError as e:
        await message.reply(f"Ошибка: {e}. Пожалуйста, введите минуты начала снова.")


@router.message(SettingsClass.setting_end_hour)
async def set_end_hour(message: Message, state: FSMContext):
    """Сохранение часа окончания рабочего дня"""
    try:
        end_hour = int(message.text)

        await state.update_data(setting_end_hour=end_hour)
        await message.reply("Введите минуты окончания рабочего дня (0-59):")
        await state.set_state(SettingsClass.setting_end_minute)
    except ValueError as e:
        await message.reply(f"Ошибка: {e}. Пожалуйста, введите час окончания снова.")


@router.message(SettingsClass.setting_end_minute)
async def set_end_minute(message: Message, state: FSMContext):
    """Сохранение минут окончания рабочего дня и запись в JSON файл"""
    try:
        end_minute = int(message.text)
        if not (0 <= end_minute <= 59):
            raise ValueError("Минуты должны быть в диапазоне от 0 до 59.")
        await state.update_data(setting_end_minute=end_minute)

        # Получаем ранее сохраненные данные
        data = await state.get_data()
        start_hour = data.get("setting_start_hour")
        start_minute = data.get("setting_start_minute")
        end_hour = data.get("setting_end_hour")
        end_minute = data.get("setting_end_minute")

        # Создаем словарь с рабочим временем
        working_hours = {
            "start": {"hour": start_hour, "minute": start_minute},
            "end": {"hour": end_hour, "minute": end_minute},
        }

        # Сохраняем словарь в JSON файл
        save_data_to_json(working_hours, WORKING_HOURS_FILE)

        await message.reply("Информация о рабочем времени обновлена.")
        # Сбрасываем состояние после успешного сохранения
        await state.clear()
    except ValueError as e:
        await message.reply(f"Ошибка: {e}. Пожалуйста, введите минуты окончания снова.")


@router.callback_query(F.data == "about_the_author")
async def about_the_author_handlers(callback_query: types.CallbackQuery) -> None:
    """Об авторе"""
    try:
        user_id = callback_query.from_user.id

        user_name = callback_query.from_user.username
        if callback_query.from_user.username is None:
            user_name = ''  # Установим пустую строку вместо None

        user_first_name = callback_query.from_user.first_name
        user_last_name = callback_query.from_user.last_name
        logger.info(f"Пользователь запросил раздел от авторе: {user_id} {user_name} {user_first_name} {user_last_name}")
        await bot.send_message(
            callback_query.from_user.id,
            load_bot_info(messages="messages/about_author.json"),
            reply_markup=back_to_menu(),
            disable_web_page_preview=True,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def register_greeting_user_handler():
    """Регистрация обработчиков для бота"""

    router.message.register(user_start_handler)
    router.message.register(instructions_handlers)  # обработчик для кнопки "Назад"
    router.message.register(edit_main_menu)  # обработчик для кнопки "Назад"
    router.message.register(update_info)
    router.message.register(start_setting_hours)
    router.message.register(set_start_hour)
    router.message.register(set_start_minute)
    router.message.register(set_end_hour)
    router.message.register(set_end_minute)

    router.message.register(about_the_author_handlers)  # Об авторе


if __name__ == "__main__":
    register_greeting_user_handler()
