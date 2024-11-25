import asyncio

from aiogram.methods import DeleteWebhook
from loguru import logger

from handlers.business_handler import register_handle_business_message

from handlers.user_handlers import register_greeting_user_handler
from system.dispatcher import bot, dp

logger.add("logs/log.log")


async def main():
    """Старт бота"""
    try:
        register_greeting_user_handler()  # Главное меню бота
        register_handle_business_message()

        try:
            await bot(DeleteWebhook(drop_pending_updates=True))
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
