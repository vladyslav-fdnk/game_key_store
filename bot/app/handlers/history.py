from aiogram import Router, F, types
from services.backend_api import BackendAPIClient
import logging

router = Router()


@router.message(F.text == "📋 История покупок")
async def show_history(message: types.Message):
    api = BackendAPIClient()
    try:
        data = await api.get_profile(message.from_user.id)
    finally:
        await api.close()

    if "error" in data:
        await message.answer("❌ Пользователь не найден")
        return

    keys = data.get("keys", [])

    if not keys:
        await message.answer("📋 У вас пока нет купленных игр.")
        return

    text = f"📋 <b>Ваши покупки ({len(keys)} шт.):</b>\n\n"

    for i, item in enumerate(keys, 1):
        date = item["updated_at"][:10]
        text += (
            f"{i}. 🎮 <b>{item['game_title']}</b>\n"
            f"    🗝️ <code>{item['key_value']}</code>\n"
            f"    📅 {date}\n\n"
        )

    await message.answer(text, parse_mode="HTML")
