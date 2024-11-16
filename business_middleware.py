from typing import Dict, Any, Awaitable, Callable

import httpx
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from opening_hours import check_opening_hours
from settings import secrets


class BusinessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{secrets.token}/getChat?chat_id={secrets.admin_id}"
            )
            chat = response.json()
            print(chat)

            # Проверяем, что в ответе есть нужные данные
            if "result" in chat:
                full_chat = chat["result"]
                print(full_chat)

                # Проверяем часы работы бизнеса
                if check_opening_hours(full_chat.get("business_opening_hours")):
                    context = data.get("event_context")
                    print(context)

                    # Проверяем наличие необходимых атрибутов
                    if (
                            context
                            and hasattr(context, 'user')
                            and context.user.id != secrets.admin_id
                            and hasattr(context, 'business_connection_id')
                    ):
                        return await handler(event, data)

        # Если условия не выполнены, просто вызываем обработчик
        return await handler(event, data)
