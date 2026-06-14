from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from games.models import Game
from users.models import TelegramUser
from orders.models import Order
from payments.services import process_successful_payment
from .serializers import GameSerializer, TelegramUserSerializer, OrderSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = "telegram_id"


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        game_id = request.data.get("game")
        try:
            game = Game.objects.get(id=game_id)
            if game.keys.filter(is_sold=False).count() == 0:
                return Response(
                    {"error": "Для данной игры больше нет ключей."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Game.DoesNotExist:
            return Response({"error": "Игра не найдена."}, status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def check_keys(self, request, pk=None):
        order = self.get_object()
        available = order.game.keys.filter(is_sold=False).count()
        if available > 0:
            return Response({"available": True})
        return Response({
            "available": False,
            "error": "😔 К сожалению, товар закончился у поставщика за время выбора."
        })

    @action(detail=True, methods=["post"])
    def complete_payment(self, request, pk=None):
        order = self.get_object()
        transaction_id = request.data.get("transaction_id")
        try:
            payment = process_successful_payment(
                order_id=order.id,
                transaction_id=transaction_id
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "key": payment.order.assigned_key.key_value,
            "game_title": payment.order.game.title,
            "amount": payment.amount,
        })