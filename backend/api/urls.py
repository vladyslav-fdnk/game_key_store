from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, TelegramUserViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'users', TelegramUserViewSet, basename='user')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]