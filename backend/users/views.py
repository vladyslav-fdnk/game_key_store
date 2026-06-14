from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import TelegramUser

@api_view(["POST"])
def get_or_create_user(request):
    data = request.data
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=data["telegram_id"],
        defaults={
            "username": data.get("username"),
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
        }
    )
    if not created:
        user.username = data.get("username")
        user.first_name = data.get("first_name", "")
        user.last_name = data.get("last_name", "")
        user.save()

    return Response({"telegram_id": user.telegram_id, "created": created})


@api_view(["GET"])
def get_profile(request, tg_id: int):

    try:
        user = TelegramUser.objects.prefetch_related("orders__assigned_key").get(
            telegram_id=tg_id
        )
    except TelegramUser.DoesNotExist:
        return Response({"error": "not found"}, status=404)

    completed_orders = user.orders.filter(status="COMPLETED")

    return Response({
        "telegram_id": user.telegram_id,
        "registered_at": user.registered_at,
        "total_orders": user.orders.count(),
        "total_spent": sum(o.amount_paid or 0 for o in completed_orders),
        "keys": [
            {
                "game_title": o.game.title,
                "key_value": o.assigned_key.key_value if o.assigned_key else None,
                "updated_at": o.updated_at
            }
            for o in completed_orders
        ]
    })