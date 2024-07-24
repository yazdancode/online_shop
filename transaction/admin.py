from django.contrib import admin
from django.contrib.admin import register

from transaction.models import Transaction, UserBalance


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "transaction_type", "amount", "created_time"]
    list_filter = ["transaction_type"]
    search_fields = ["user__username"]


@register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "created_time"]
    search_fields = ["user__username"]
