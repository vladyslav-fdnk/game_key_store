from aiogram import Router, F, types
from aiogram.types import LabeledPrice, PreCheckoutQuery
from services.backend_api import BackendAPIClient

router = Router()


@router.callback_query(F.data.startswith("buy_game_"))
async def process_buy_game(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[2])
    tg_id = callback.from_user.id

    api = BackendAPIClient()
    try:
        data = await api.create_order(user_id=tg_id, game_id=game_id)
    finally:
        await api.close()

    if data.get("error") == "Игра не найдена." or data.get("status_code") == 404:
        await callback.answer("❌ Системный сбой: игра не найдена.", show_alert=True)
        return
    elif data.get("error") == "Для данной игры больше нет ключей.":
        await callback.answer("😔 Извините, все ключи уже распроданы!", show_alert=True)
        return
    elif "id" not in data:
        await callback.answer("❌ Ошибка сервера. Попробуйте позже.", show_alert=True)
        return

    order_id = data["id"]
    game_title = data.get("game_title", "Игра")
    price_stars = data.get("price_stars", 1)

    await callback.message.answer_invoice(
        title=f"Покупка: {game_title}",
        description=f"Лицензионный ключ Steam для '{game_title}'. Моментальная выдача после оплаты.",
        payload=f"order_{order_id}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"Покупка '{game_title}'", amount=price_stars)],
        start_parameter="buy-steam-key"
    )
    await callback.answer()


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    order_id = int(pre_checkout_query.invoice_payload.split("_")[1])

    api = BackendAPIClient()
    try:
        data = await api.check_order_keys(order_id)
    finally:
        await api.close()

    if data.get("available"):
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(
            ok=False,
            error_message=data.get("error", "Товар недоступен.")
        )


@router.message(F.successful_payment)
async def process_successful_billing(message: types.Message):
    payment_info = message.successful_payment
    order_id = int(payment_info.invoice_payload.split("_")[1])
    telegram_charge_id = payment_info.telegram_payment_charge_id

    api = BackendAPIClient()
    try:
        data = await api.complete_payment(order_id=order_id, transaction_id=telegram_charge_id)
    finally:
        await api.close()

    if data.get("status_code") != 200:
        await message.answer(
            f"⚠️ Оплата прошла, но возникла ошибка при выдаче ключа.\n"
            f"Обратитесь в поддержку с ID заказа: #{order_id}."
        )
        return

    await message.answer(
        f"🎉 <b>Оплата успешно подтверждена!</b>\n"
        f"Списано: ⭐ {data['amount']} Stars\n"
        f"ID платежа: <code>{telegram_charge_id}</code>\n\n"
        f"🎮 Ваша игра: <b>{data['game_title']}</b>\n"
        f"🗝️ Ключ активации Steam:\n"
        f"<code>{data['key']}</code>\n\n"
        f"💡 <i>Зажмите ключ пальцем, чтобы скопировать. Активируйте в Steam на ПК!</i>",
        parse_mode="HTML"
    )