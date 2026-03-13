from django.contrib import admin
from .models import Signal


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ("asset", "strategy", "signal_type", "price", "timestamp")
    list_filter = ("strategy", "signal_type")
    search_fields = ("asset__symbol", "strategy")