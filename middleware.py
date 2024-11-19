from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware

from aiogram.types import Message



class ChatTypeMiddleware(BaseMiddleware):  # [1]
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if event.chat.type != 'private':
            return
        else:
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
            result = await handler(event, data)
            return result