import datetime
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message




# Это будет outer-мидлварь на любые колбэки
class WeekendCallbackMiddleware(BaseMiddleware):
    def is_weekend(self) -> bool:
        # 5 - суббота, 6 - воскресенье
        return datetime.datetime.now(datetime.UTC).weekday() in (5, 6)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if not self.is_weekend():
            return await handler(event, data)
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
        await event.answer(
            "Какая работа? Завод остановлен до понедельника!",
            show_alert=True
        )
        return

