from aiogram import Router, types, F
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from users.services import get_user_profile_data_sync

router = Router()

@router.message(Command("profile"))
async def show_profile(message: types.Message):
    await message.answer("PROFILE WORKS")

@router.message(F.text == "👤 Мой профиль")
@router.message(Command("profile"))
async def show_profile(message: types.Message):
    print("PROFILE HANDLER WORKS")

    tg_id = message.from_user.id

    profile_data = await sync_to_async(get_user_profile_data_sync)(tg_id)

    if not profile_data:
        await message.answer("❌ Пользователь не найден")
        return

    text = (
        f"👤 Профиль- {message.from_user.username}\n\n"
        f"ID: {profile_data['telegram_id']}\n"
        f"📅 Регистрация: {profile_data['registered_at']}\n"
        f"📦 Заказов: {profile_data['total_orders']}\n"
        f"💰 Потрачено: {profile_data['total_spent']} Stars\n"
    )

    await message.answer(text)