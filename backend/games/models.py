from django.db import models

class Game(models.Model):
    title = models.CharField("Название игры", max_length=255, unique=True)
    description = models.TextField("Описание игры", blank=True)
    price_stars = models.PositiveIntegerField("Цена в Telegram Stars", default=10)
    image_url = models.URLField("Ссылка на обложку", blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_keys = None

    def __str__(self):
        return self.title

    @property
    def available_keys_count(self):

        return self.keys.filter(is_sold=False).count()


class SteamKey(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="keys",
        verbose_name="Игра"
    )
    key_value = models.CharField("Ключ активации", max_length=255, unique=True)
    is_sold = models.BooleanField("Ключ продан", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Steam Ключ"
        verbose_name_plural = "Steam Ключи"

    def __str__(self):
        return f"{self.game.title} - {'[ПРОДАН]' if self.is_sold else '[СВОБОДЕН]'}"