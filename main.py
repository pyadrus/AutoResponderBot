import asyncio

from aiogram.methods import DeleteWebhook
from loguru import logger

from handlers.business_handler import register_handle_business_message
from handlers.events import start_bot, stop_bot
from handlers.setting_handlers import register_setting_handlers
from handlers.user_handlers import register_greeting_user_handler
from system.dispatcher import bot, dp

logger.add("logs/log.log")


async def main():
    """Старт бота"""
    try:
        register_greeting_user_handler()  # Главное меню бота
        register_setting_handlers()  # Изменение настроек

        dp.startup.register(start_bot)  # Сообщение о старте бота.
        dp.shutdown.register(stop_bot)  # Сообщение об остановке бота.

        # dp.business_message.register(handle_business_message)
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
