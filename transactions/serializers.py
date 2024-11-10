from rest_framework import serializers
from .models import Transaction
from categories.models import Category, SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    subcategory_id = serializers.IntegerField(write_only=True)

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