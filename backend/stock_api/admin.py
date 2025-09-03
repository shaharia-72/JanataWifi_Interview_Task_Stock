from django.contrib import admin

from .models import stockModel


@admin.register(stockModel)
class StockAdmin(admin.ModelAdmin):
    list_display = ['trade_code', 'date', 'open_trade', 'high_trade', 'low_trade', 'close_trade', 'volume']
    list_filter = ['trade_code', 'date']
    search_fields = ['trade_code', 'date']
    ordering = ['-date', 'trade_code']
    list_per_page = 50
