import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем конфигурации из локального файла
from bot_config import BOT_TOKEN
from handlers import start
#, catalog, profile, purchase)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    # Инициализация бота с парсингом HTML по умолчанию
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем роутеры хэндлеров по этапам
    dp.include_router(start.router)
    # dp.include_router(catalog.router)
    # dp.include_router(profile.router)
    # dp.include_router(purchase.router)

    logging.info("Telegram Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())