import asyncio

from aiogram import Dispatcher
from aiogram.methods import DeleteWebhook

from business_handler import handle_business_message
from events import start_bot, stop_bot
from settings import bot


async def start():
    """Start bot"""
    dp = Dispatcher()

    dp.startup.register(start_bot)  # Сообщение о старте бота.
    dp.shutdown.register(stop_bot)  # Сообщение об остановке бота.

    dp.business_message.register(handle_business_message)

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
