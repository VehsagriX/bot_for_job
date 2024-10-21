import asyncio
import logging
from aiogram import Bot
from aiogram import Dispatcher
from config import settings
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import command_handlers, user_handlers, registration_handlers
from aiogram.utils.chat_action import ChatActionMiddleware

from middleware import WeekendCallbackMiddleware


# вам что то испправить - you need to fix something
# вам что то приобрести - buy something for you


async def main():
    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ChatActionMiddleware())
    dp.message.outer_middleware(WeekendCallbackMiddleware())
    dp.include_routers(command_handlers.router, registration_handlers.router, user_handlers.router)
    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
