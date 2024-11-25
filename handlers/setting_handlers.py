from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from state_group.state_group import SettingsClass
from system.dispatcher import ADMIN_CHAT_ID
from system.dispatcher import bot
from system.dispatcher import router
from system.working_with_files import save_to_json

# ADMIN_CHAT_ID должен быть списком строк, а не чисел
ADMIN_CHAT_ID = ["535185511"]

# Путь к JSON файлу, где будут храниться рабочие часы
WORKING_HOURS_FILE = 'messages/working_hours.json'





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
        save_to_json(working_hours, WORKING_HOURS_FILE)

        await message.reply("Информация о рабочем времени обновлена.")
        # Сбрасываем состояние после успешного сохранения
        await state.clear()
    except ValueError as e:
        await message.reply(f"Ошибка: {e}. Пожалуйста, введите минуты окончания снова.")


def register_setting_handlers():
    """Регистрация обработчиков для бота"""
    router.message.register(start_setting_hours)
    router.message.register(set_start_hour)
    router.message.register(set_start_minute)
    router.message.register(set_end_hour)
    router.message.register(set_end_minute)


if __name__ == "__main__":
    register_setting_handlers()