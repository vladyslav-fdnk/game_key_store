from aiogram import Router, F, types
from aiogram.types import LabeledPrice
from services.backend_api import BackendAPIClient
import json
import logging

router = Router()


@router.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    data = json.loads(message.web_app_data.data)

    if data.get("action") != "buy_web_app":
        return

    game_id = data["game_id"]
    tg_id = message.from_user.id

    api = BackendAPIClient()
    try:
        order = await api.create_order(user_id=tg_id, game_id=game_id)
    finally:
        await api.close()

    if "error" in order:
        await message.answer(f"❌ {order['error']}")
        return

    order_id = order["id"]
    game_title = order.get("game_title", "Игра")
    price_stars = order.get("price_stars", 1)

    await message.answer_invoice(
        title=f"Покупка: {game_title}",
        description=f"Лицензионный ключ Steam для '{game_title}'.",
        payload=f"order_{order_id}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=game_title, amount=price_stars)],
        start_parameter="buy-steam-key"
    )