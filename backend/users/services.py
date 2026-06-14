from users.models import TelegramUser


def get_user_profile_data_sync(tg_id):
    try:
        user = TelegramUser.objects.prefetch_related(
            "orders__assigned_key"
        ).get(telegram_id=tg_id)
    except TelegramUser.DoesNotExist:
        return None

    completed_orders = list(
        user.orders.filter(status="COMPLETED")
        .select_related("game", "assigned_key")
    )

    total_orders = user.orders.count()

    total_spent = sum(
        order.amount_paid or 0 for order in completed_orders
    )

    keys_data = [
        {
            "game_title": order.game.title,
            "key_value": order.assigned_key.key_value if order.assigned_key else "нет ключа",
            "updated_at": order.updated_at.strftime('%d.%m %H:%M')
        }
        for order in completed_orders
    ]

    return {
        "telegram_id": user.telegram_id,
        "registered_at": user.registered_at.strftime('%Y-%m-%d %H:%M'),
        "total_orders": total_orders,
        "total_spent": total_spent,
        "keys": keys_data
    }