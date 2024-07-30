from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    """
    Represents a transaction made by a user.
    """

    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SENT = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER_SENT, "Transfer sent"),
        (TRANSFER_RECEIVED, "Transfer received"),
    )

    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.RESTRICT
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES, default=CHARGE
    )
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"

    @classmethod
    def get_report(cls):
        """
        Generates a report of all users with their transaction counts and balances.
        """
        positive_transactions = Sum(
            "transactions__amount",
            filter=Q(
                transactions__transaction_type__in=[cls.CHARGE, cls.TRANSFER_RECEIVED]
            ),
        )
        negative_transactions = Sum(
            "transactions__amount",
            filter=Q(
                transactions__transaction_type__in=[cls.PURCHASE, cls.TRANSFER_SENT]
            ),
        )

        users = User.objects.annotate(
            transaction_count=Count("transactions__id"),
            balance=Coalesce(positive_transactions, 0)
            - Coalesce(negative_transactions, 0),
        )
        return users

    @classmethod
    def get_total_balance(cls):
        """
        Calculates the total balance of all users.
        """
        queryset = cls.get_report()
        return queryset.aggregate(total_balance=Sum("balance"))

    @classmethod
    def user_balance(cls, user):
        """
        Calculates the balance for a specific user.
        """
        positive_transactions = Sum(
            "amount", filter=Q(transaction_type__in=[cls.CHARGE, cls.TRANSFER_RECEIVED])
        )
        negative_transactions = Sum(
            "amount", filter=Q(transaction_type__in=[cls.PURCHASE, cls.TRANSFER_SENT])
        )

        user_balance = user.transactions.aggregate(
            balance=Coalesce(positive_transactions, 0)
            - Coalesce(negative_transactions, 0)
        )
        return user_balance.get("balance", 0)


class UserBalance(models.Model):
    """
    Represents the balance of a user at a specific time.
    """

    user = models.ForeignKey(
        User, related_name="balance_records", on_delete=models.PROTECT
    )
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"

    @classmethod
    def record_user_balance(cls, user):
        """
        Records the current balance of a user.
        """
        balance = Transaction.user_balance(user=user)
        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def record_all_users_balance(cls):
        """
        Records the balance of all users.
        """
        users = User.objects.all()
        user_balances = [
            cls(user=user, balance=Transaction.user_balance(user=user))
            for user in users
        ]
        cls.objects.bulk_create(user_balances)


class TransferTransactions(models.Model):
    """
    Represents a transfer transaction between two users.
    """

    sender_transaction = models.ForeignKey(
        Transaction, related_name="sent_transfers", on_delete=models.RESTRICT
    )
    receiver_transaction = models.ForeignKey(
        Transaction, related_name="received_transfers", on_delete=models.RESTRICT
    )

    def __str__(self):
        return f"{self.sender_transaction} >> {self.receiver_transaction}"

    @classmethod
    def transfer(cls, sender, receiver, amount):
        """
        Transfers a specified amount from the sender to the receiver.
        """
        if Transaction.user_balance(sender) < amount:
            return "Transaction not allowed, insufficient balance"

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender, amount=amount, transaction_type=Transaction.TRANSFER_SENT
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver,
                amount=amount,
                transaction_type=Transaction.TRANSFER_RECEIVED,
            )
            instance = cls.objects.create(
                sender_transaction=sender_transaction,
                receiver_transaction=receiver_transaction,
            )

        return instance


class UserScore(models.Model):
    """
    Represents the score of a user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        permissions = [("has_score_permission", "Has  Score permission")]

    @classmethod
    def change_score(cls, user, score):
        """
        Changes the score of a user.
        """
        with transaction.atomic():
            instance, created = cls.objects.select_for_update().get_or_create(user=user)
            instance.score += score
            instance.save()
