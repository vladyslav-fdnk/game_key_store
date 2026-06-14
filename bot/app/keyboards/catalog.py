from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_games_list_keyboard(games: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for game in games:
        keys_count = game.get("keys_available", 0)
        status = "✅" if keys_count > 0 else "❌"
        builder.button(
            text=f"{status} {game['title']} — ⭐{game['price_stars']}",
            callback_data=f"game_detail_{game['id']}"
        )
    builder.adjust(1)
    return builder.as_markup()


def get_game_detail_keyboard(game_id: int, show_buy_btn: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if show_buy_btn:
        builder.button(
            text="⭐ Купить за Stars",
            callback_data=f"buy_game_{game_id}"
        )
    else:
        builder.button(
            text="🔔 Уведомить о поступлении",
            callback_data=f"notify_game_{game_id}"
        )
    builder.button(text="◀️ Назад к каталогу", callback_data="back_to_catalog")
    builder.adjust(1)
    return builder.as_markup()