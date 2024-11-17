from django.db import models
from categories.models import Category
from users.models import Profile


class Budget(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name='budgets',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        related_name='budgets',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.category:
            return f"{self.name} - {self.category.name}"
        return self.name
