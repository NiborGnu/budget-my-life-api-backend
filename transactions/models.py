from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.transaction_type.capitalize()}: {self.amount} "
            f"by {self.profile.user.username}"
        )