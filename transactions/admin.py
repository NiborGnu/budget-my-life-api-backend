from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'transaction_type',
        'amount',
        'category',
        'subcategory',
        'budget',
        'created_at'
    )
    search_fields = ('profile__owner__username', 'description')
    list_filter = ('transaction_type', 'category', 'created_at')
