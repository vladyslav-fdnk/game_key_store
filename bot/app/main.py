import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем конфигурации из локального файла
from bot_config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.catalog import router as catalog_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    # Инициализация бота с парсингом HTML по умолчанию
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем роутеры хэндлеров по этапам
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    # dp.include_router(profile.router)
    # dp.include_router(purchase.router)

    logging.info("Telegram Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())