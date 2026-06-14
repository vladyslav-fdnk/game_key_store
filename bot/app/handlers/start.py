from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from asgiref.sync import sync_to_async

import sys
import os

# Добавляем путь к Django, чтобы была доступна ORM (пока общаемся напрямую)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../backend'))
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import TelegramUser

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    tg_user = message.from_user

    # 🌟 Бизнес-логика: Сохраняем пользователя в Базу Данных
    user, created = await sync_to_async(
        TelegramUser.objects.get_or_create
    )(
        telegram_id=tg_user.id,
        defaults={
            "username": tg_user.username,
            "first_name": tg_user.first_name or "",
            "last_name": tg_user.last_name or "",
        }
    )

    if not created:
        user.username = tg_user.username
        user.first_name = tg_user.first_name or ""
        user.last_name = tg_user.last_name or ""

        await sync_to_async(user.save)()

    # Готовим кнопки главного меню
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎮 Каталог игр")
    builder.button(text="👤 Мой профиль")
    builder.adjust(2)

    welcome_text = (
        f"👋 Привет, {tg_user.first_name}!\n\n"
        f"Добро пожаловать в самый быстрый <b>Steam Key Store</b> в Telegram! \n"
        f"Здесь вы можете приобрести лицензионные ключи активации ваших любимых игр за ⭐ <b>Telegram Stars</b>.\n\n"
        f"Пользуйтесь меню ниже для просмотра каталога!"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=builder.as_markup(resize_keyboard=True)
    )