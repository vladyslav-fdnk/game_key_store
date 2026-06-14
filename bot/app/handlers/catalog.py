from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.catalog import get_games_list_keyboard, get_game_detail_keyboard
from services.backend_api import BackendAPIClient
import logging

router = Router()


@router.message(F.text == "🎮 Каталог игр")
@router.message(Command("catalog"))
async def show_catalog(message: types.Message):
    logging.info("CATALOG HANDLER CALLED")
    api = BackendAPIClient()
    try:
        games = await api.get_games()
    finally:
        await api.close()

    if not games:
        await message.answer("😔 Сейчас нет доступных игр. Заходите позже!")
        return

    await message.answer(
        "🎮 <b>Каталог игр</b>\n\nВыберите игру для подробной информации:",
        reply_markup=get_games_list_keyboard(games),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("game_detail_"))
async def show_game_detail(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[2])

    api = BackendAPIClient()
    try:
        games = await api.get_games()
    finally:
        await api.close()

    game = next((g for g in games if g["id"] == game_id), None)
    if not game:
        await callback.answer("Игра не найдена", show_alert=True)
        return

    keys_count = game.get("keys_available", 0)
    status_text = f"✅ Доступно: <b>{keys_count} шт.</b>" if keys_count > 0 else "❌ Нет в наличии"

    info_text = (
        f"🎮 <b>{game['title']}</b>\n\n"
        f"📝 <i>{game.get('description') or 'Описание скоро появится.'}</i>\n\n"
        f"💰 Стоимость: ⭐ <b>{game['price_stars']} Stars</b>\n"
        f"📦 Наличие: {status_text}"
    )

    keyboard = get_game_detail_keyboard(game["id"], show_buy_btn=(keys_count > 0))

    if game.get("image_url"):
        try:
            await callback.message.answer_photo(
                photo=game["image_url"],
                caption=info_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            await callback.message.delete()
        except Exception:
            await callback.message.edit_text(info_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.message.edit_text(info_text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: types.CallbackQuery):
    api = BackendAPIClient()
    try:
        games = await api.get_games()
    finally:
        await api.close()

    text = "🎮 <b>Каталог игр</b>\n\nВыберите игру для подробной информации:"
    keyboard = get_games_list_keyboard(games)

    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:

        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()