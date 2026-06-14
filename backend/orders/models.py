from django.db import models
from users.models import TelegramUser
from games.models import Game, SteamKey


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "В ожидании оплаты"
        COMPLETED = "COMPLETED", "Оплачено"
        FAILED = "FAILED", "Ошибка"

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь"
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Игра"
    )

    assigned_key = models.ForeignKey(
        SteamKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Выданный ключ"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    amount_paid = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} | {self.user} - {self.game.title}"