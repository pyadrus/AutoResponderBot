from settings import bot, secrets


def start_bot_message():
    return "Бот запущен"


def stop_bot_message():
    return "Бот остановлен"


async def start_bot():
    await bot.send_message(secrets.admin_id, start_bot_message())


async def stop_bot():
    await bot.send_message(secrets.admin_id, stop_bot_message())
