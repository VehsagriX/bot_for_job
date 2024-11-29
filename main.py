import asyncio
import logging
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import command_handlers, request_handler, registration_handlers, callback_handler, edit_profile, \
    admin_work, Vaucher
from aiogram.utils.chat_action import ChatActionMiddleware

from middleware import ChatTypeMiddleware

bot = Bot(token=settings.bot_test_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))




async def main():
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    dp.message.outer_middleware(ChatTypeMiddleware())
    dp.message.middleware(ChatActionMiddleware())

    dp.include_routers(command_handlers.router,
                       request_handler.router,
                       registration_handlers.router,
                       edit_profile.router,
                       admin_work.router,
                       Vaucher.router,
                       callback_handler.router)

    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
