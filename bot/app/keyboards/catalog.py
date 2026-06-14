from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_catalog_keyboard(game_id: int, show_buy_btn: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if show_buy_btn:
        # Уникальный callback_data для инициации процесса оплаты
        builder.button(
            text="🛒 Купить за Stars",
            callback_data=f"buy_game_{game_id}"
        )
    else:
        builder.button(
            text="🔔 Сообщить о поступлении",
            callback_data=f"notify_game_{game_id}"
        )

    return builder.as_markup()