import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot_config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.catalog import router as catalog_router
from handlers.profile import router as profile_router
from handlers.purchase import router as purchase_router
from handlers.history import router as history_router
from handlers.webapp import router as webapp_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(profile_router)
    dp.include_router(purchase_router)
    dp.include_router(history_router)
    dp.include_router(webapp_router)

    logging.info("Telegram бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())