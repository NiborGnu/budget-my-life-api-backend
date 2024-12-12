from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'amount',
        'profile',
        'category',
        'created_at',
        'updated_at'
    )
    search_fields = ('name', 'profile__owner__username')
    list_filter = ('category', 'created_at')
