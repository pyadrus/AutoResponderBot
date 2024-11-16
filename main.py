import asyncio

from aiogram import Dispatcher
from aiogram.methods import DeleteWebhook

from business_handler import handle_business_message
from events import start_bot, stop_bot
from business_middleware import BusinessMiddleware
from settings import bot


async def start():
    dp = Dispatcher()

    dp.update.middleware(BusinessMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.business_message.register(handle_business_message)

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
