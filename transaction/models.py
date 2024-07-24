from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER = 3

    Transaction_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER, "Transfer"),
    )

    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.RESTRICT
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=Transaction_TYPE_CHOICES, default=CHARGE
    )
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        """Show all users and their balance"""
        positive_transactions = Sum(
            "transactions__amount", filter=Q(transactions__transaction_type=cls.CHARGE)
        )
        negative_transactions = Sum(
            "transactions__amount",
            filter=Q(transactions__transaction_type__in=[cls.PURCHASE, cls.TRANSFER]),
        )
        users = User.objects.all().annotate(
            transaction_count=Count("transactions__id"),
            balance=Coalesce(positive_transactions, 0)
            - Coalesce(negative_transactions, 0),
        )
        return users

    @classmethod
    def get_total_balance(cls):
        queryset = cls.get_report()
        return queryset.aggregate(Sum("balance"))


class UserBalance(models.Model):
    user = models.ForeignKey(
        User, related_name="balance_records", on_delete=models.PROTECT
    )
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"
