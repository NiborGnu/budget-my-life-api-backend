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
            'description',
            'created_at'
        ]
