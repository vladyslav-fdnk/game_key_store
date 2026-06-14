from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order
from users.models import TelegramUser
from games.models import Game
from payments.services import process_successful_payment


@api_view(["POST"])
def create_order(request):
    game_id = request.data.get("game_id")
    tg_id = request.data.get("tg_id")

    try:
        game = Game.objects.get(id=game_id)
        user = TelegramUser.objects.get(telegram_id=tg_id)
    except (Game.DoesNotExist, TelegramUser.DoesNotExist):
        return Response({"error": "not_found"}, status=404)

    available = game.keys.filter(is_sold=False).count()
    if available == 0:
        return Response({"error": "no_keys"}, status=400)

    order = Order.objects.create(user=user, game=game, status="PENDING")

    return Response({
        "order_id": order.id,
        "game_title": game.title,
        "price_stars": game.price_stars,
    })


@api_view(["GET"])
def check_order_keys(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Заказ не найден"}, status=404)

    available = order.game.keys.filter(is_sold=False).count()
    if available > 0:
        return Response({"available": True})
    else:
        return Response({"available": False, "error": "😔 К сожалению, товар закончился у поставщика за время выбора."})


@api_view(["POST"])
def complete_payment(request, order_id):
    transaction_id = request.data.get("transaction_id")

    try:
        payment = process_successful_payment(
            order_id=order_id,
            transaction_id=transaction_id
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({
        "key": payment.order.assigned_key.key_value,
        "game_title": payment.order.game.title,
        "amount": payment.amount,
    })