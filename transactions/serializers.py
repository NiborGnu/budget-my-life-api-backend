from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Transaction
        fields = [
            'id',
            'profile',
            'amount',
            'transaction_type',
            'category',
            'subcategory',
            'category_id',
            'subcategory_id',
            'description',
            'created_at'
        ]
