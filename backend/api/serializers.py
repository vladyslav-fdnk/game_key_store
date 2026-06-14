from rest_framework import serializers
from games.models import Game
from users.models import TelegramUser
from orders.models import Order


class GameSerializer(serializers.ModelSerializer):
    keys_available = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "title", "description", "price_stars", "image_url", "keys_available"]

    def get_keys_available(self, obj):
        return obj.keys.filter(is_sold=False).count()


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["telegram_id", "username", "first_name", "last_name", "registered_at"]


class OrderSerializer(serializers.ModelSerializer):
    key_value = serializers.CharField(source="assigned_key.key_value", read_only=True)
    game_title = serializers.CharField(source="game.title", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "game", "game_title", "key_value", "status", "amount_paid", "created_at"]