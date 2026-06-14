from aiogram import Router, F, types
from aiogram.filters import Command
from django.db.models import Q, Count

from games.models import Game
from keyboards.catalog import get_catalog_keyboard

from asgiref.sync import sync_to_async

import logging

router = Router()


@router.message(F.text == "🎮 Каталог игр")
@router.message(Command("catalog"))
async def show_catalog(message: types.Message):
    logging.info("CATALOG HANDLER CALLED")
    # Берем только игры, у которых есть непроданные ключи
    games = await sync_to_async(
        lambda: list(
            Game.objects.annotate(
                available_keys=Count(
                    "keys",
                    filter=Q(keys__is_sold=False)
                )
            )
        )
    )()

    if not games:
        await message.answer(
            "😔 Извините, но сейчас нет доступных игр. Загляните позже!"
        )
        return

    await message.answer("🎮 Доступные игры в каталоге:")

    for game in games:
        keys_count = game.available_keys
        status_text = f"💚 В наличии: <b>{keys_count} шт.</b>" if keys_count > 0 else "🔴 Нет в наличии"

        info_text = (
            f"🎬 <b>{game.title}</b>\n\n"
            f"📝 <i>{game.description or 'Описание временно отсутствует.'}</i>\n\n"
            f"💵 Стоимость: ⭐ <b>{game.price_stars} Stars</b>\n"
            f"ℹ️ Статус: {status_text}"
        )

        keyboard = get_catalog_keyboard(game.id, show_buy_btn=(keys_count > 0))

        if game.image_url:
            try:
                await message.answer_photo(
                    photo=game.image_url,
                    caption=info_text,
                    reply_markup=keyboard
                )
            except Exception:
                # На случай битой ссылки на обложку
                await message.answer(text=info_text, reply_markup=keyboard)
        else:
            await message.answer(text=info_text, reply_markup=keyboard)