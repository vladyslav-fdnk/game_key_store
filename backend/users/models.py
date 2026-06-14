from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField("Telegram ID", unique=True, primary_key=True)
    username = models.CharField("Юзернейм", max_length=150, blank=True, null=True)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    is_active = models.BooleanField("Активен в боте", default=True)
    registered_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ["-registered_at"]

    def __str__(self):
        if self.username:
            return f"@{self.username} ({self.first_name})"
        return f"ID: {self.telegram_id} ({self.first_name})"