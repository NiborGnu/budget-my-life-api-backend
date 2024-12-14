from django.db import models


class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=25, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
