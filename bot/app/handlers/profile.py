from aiogram import Router, F, types
from services.backend_api import BackendAPIClient

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def profile(message: types.Message):
    api = BackendAPIClient()
    try:
        data = await api.get_profile(message.from_user.id)
    finally:
        await api.close()

    if "error" in data:
        await message.answer("❌ Пользователь не найден")
        return

    await message.answer(
        f"👤 Профиль: @{message.from_user.username}\n\n"
        f"ID: {data['telegram_id']}\n"
        f"📅 Зарегистрирован: {data['registered_at']}\n"
        f"🛒 Заказов: {data['total_orders']}\n"
        f"💰 Потрачено: {data['total_spent']} Stars\n",
        parse_mode="HTML"
    )