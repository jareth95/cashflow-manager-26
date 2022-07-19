from django.contrib import admin
from .models import Investment


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'exchange', 'owner', 'buy_date', 'sell_date')
    search_fields = ('name', 'exchange', 'owner')
    list_per_page = 10


admin.site.register(Investment)