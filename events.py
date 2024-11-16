from settings import bot, secrets


def start_bot_message():
    return "Бот запущен"


def stop_bot_message():
    return "Бот остановлен"


def system_prompt():
    return """Ты бот помощник и ты должен помогать людям. Если тебе написали в не рабочее время, то ты должен ответить, что я отвечу позже"""


async def start_bot():
    await bot.send_message(secrets.admin_id, start_bot_message())


async def stop_bot():
    await bot.send_message(secrets.admin_id, stop_bot_message())
