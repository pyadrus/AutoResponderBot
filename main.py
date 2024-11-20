import asyncio

from aiogram.methods import DeleteWebhook

from handlers.business_handler import handle_business_message
from handlers.events import start_bot, stop_bot
from handlers.user_handlers import register_greeting_user_handler
from system.dispatcher import bot, dp


async def main():
    """Старт бота"""

    dp.startup.register(start_bot)  # Сообщение о старте бота.
    dp.shutdown.register(stop_bot)  # Сообщение об остановке бота.

    dp.business_message.register(handle_business_message)

    register_greeting_user_handler()  # Главное меню бота

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
