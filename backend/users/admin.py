from django.contrib import admin
from .models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "first_name", "registered_at", "is_active")
    list_filter = ("registered_at", "is_active")
    search_fields = ("telegram_id", "username", "first_name")
    readonly_fields = ("registered_at",)