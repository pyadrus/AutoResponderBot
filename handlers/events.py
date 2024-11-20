from system.dispatcher import bot, ADMIN_CHAT_ID


def start_bot_message():
    return "Бот запущен"


def stop_bot_message():
    return "Бот остановлен"


async def start_bot():
    await bot.send_message(ADMIN_CHAT_ID, start_bot_message())


async def stop_bot():
    await bot.send_message(ADMIN_CHAT_ID, stop_bot_message())
