from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from services.backend_api import BackendAPIClient
import logging

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    logging.info("START HANDLER CALLED")
    tg_user = message.from_user

    api = BackendAPIClient()
    try:
        await api.get_or_create_user(
            telegram_id=tg_user.id,
            username=tg_user.username or "",
            first_name=tg_user.first_name or "",
            last_name=tg_user.last_name or "",
        )
    except Exception as e:
        logging.error(f"Ошибка при создании пользователя: {e}")
    finally:
        await api.close()

    builder = ReplyKeyboardBuilder()
    builder.button(text="🎮 Каталог игр")
    builder.button(text="👤 Мой профиль")
    builder.button(text="📋 История покупок")
    builder.adjust(2)
    
    await message.answer(
        text=(
            f"👋 Привет, {tg_user.first_name}!\n\n"
            f"Добро пожаловать в <b>Steam Key Store</b>!\n"
            f"Здесь вы можете купить ключи активации игр за <b>Telegram Stars</b>.\n\n"
            f"Используйте меню ниже для навигации!"
        ),
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )