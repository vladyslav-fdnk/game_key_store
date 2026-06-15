from django.contrib import admin
from .models import Game, SteamKey

class SteamKeyInline(admin.TabularInline):
    model = SteamKey
    extra = 3
    fields = ("key_value", "is_sold")
    readonly_fields = ("is_sold",)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "price_stars", "created_at")
    search_fields = ("title",)
    inlines = [SteamKeyInline]

@admin.register(SteamKey)
class SteamKeyAdmin(admin.ModelAdmin):
    list_display = ("key_value", "game", "is_sold", "created_at")
    list_filter = ("is_sold", "game")
    search_fields = ("key_value",)