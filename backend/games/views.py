from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Q
from games.models import Game


@api_view(["GET"])
def get_games(request):
    games = Game.objects.annotate(
        available_keys=Count("keys", filter=Q(keys__is_sold=False))
    )
    data = [
        {
            "id": game.id,
            "title": game.title,
            "description": game.description,
            "price_stars": game.price_stars,
            "image_url": game.image_url,
            "available_keys": game.available_keys,
        }
        for game in games
    ]
    return Response(data)