from django.db import transaction
from .models import Payment
from orders.models import Order
from games.models import SteamKey


def process_successful_payment(order_id: int, transaction_id: str, provider: str = "STARS"):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)

        # Назначаем свободный ключ если ещё не назначен
        if not order.assigned_key:
            key = SteamKey.objects.select_for_update().filter(
                game=order.game, is_sold=False
            ).first()
            if not key:
                raise Exception("Нет доступных ключей")
            key.is_sold = True
            key.save()
            order.assigned_key = key

        order.status = "COMPLETED"
        order.amount_paid = order.game.price_stars
        order.save()

        payment, created = Payment.objects.get_or_create(
            order=order,
            transaction_id=transaction_id,
            defaults={
                "provider": provider,
                "amount": order.amount_paid,
                "status": "PAID",
            }
        )
        if not created:
            payment.status = "PAID"
            payment.save()

        return payment