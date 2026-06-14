from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Order
from games.models import SteamKey


def issue_key(order: Order) -> SteamKey:
    """
    ⚡️ САМАЯ ВАЖНАЯ БИЗНЕС-ЛОГИКА ПРОЕКТА.
    Атомарная выдача ключа для оплаченного заказа с защитой от двойных продаж (Race Condition).
    Мы блокируем строки свободных ключей для данной игры с помощью select_for_update().
    """
    # Если ключ уже выдан, отдаем его повторно без изменения базы
    if order.assigned_key:
        return order.assigned_key

    # Открываем транзакцию
    with transaction.atomic():
        # Блокируем СВОБОДНЫЕ ключи для этой конкретной игры на уровне базы данных PostgreSQL.
        # select_for_update() гарантирует, что другие параллельные потоки подождут завершения транзакции
        free_key_qs = (
            SteamKey.objects
            .select_for_update()
            .filter(game=order.game, is_sold=False)
        )

        # Берем самый первый доступный ключ
        available_key = free_key_qs.first()

        if not available_key:
            # Ключей физически нет! Отменяем заказ
            order.status = "FAILED"
            order.save()
            raise ValidationError(f"Извините, для игры '{order.game.title}' закончились цифровые ключи.")

        # Помечаем ключ проданным
        available_key.is_sold = True
        available_key.save()

        # Привязываем ключ к текущему заказу и переводим статус
        order.assigned_key = available_key
        order.status = "COMPLETED"
        order.amount_paid = order.game.price_stars
        order.save()

        return available_key