from django.db import models
from orders.models import Order


class Payment(models.Model):
    PROVIDER_CHOICES = [
        ("TEST", "Тестовый платёж"),
        ("STARS", "Telegram Stars"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "В ожидании"),
        ("PAID", "Успешно оплачен"),
        ("FAILED", "Ошибка оплаты"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True
    )
    provider = models.CharField("Провайдер оплаты", max_length=50, choices=PROVIDER_CHOICES, default="TEST")
    transaction_id = models.CharField("ID транзакции", max_length=255, blank=True)
    amount = models.PositiveIntegerField("Сумма транзакции (Stars)")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"Транзакция по заказу #{self.order.id} | {self.status} ({self.amount} Stars)"