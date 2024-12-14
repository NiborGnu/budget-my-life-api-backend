from rest_framework import serializers
from .models import Transaction
from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer, SubCategorySerializer
from budgets.models import Budget


class TransactionSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    # We only show the budget_id here, but not the full Budget object
    budget_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

    category_id = serializers.IntegerField(write_only=True, required=True)
    subcategory_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'profile',
            'amount',
            'transaction_type',
            'category',
            'subcategory',
            'budget_id',  # Display only the budget_id, not the full budget
            'category_id',
            'subcategory_id',
            'description',
            'created_at',
        ]

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        subcategory_id = validated_data.pop('subcategory_id', None)
        budget_id = validated_data.pop('budget_id', None)
        profile = self.context['request'].user.profile

        if category_id:
            validated_data['category'] = Category.objects.get(id=category_id)
        if subcategory_id:
            validated_data['subcategory'] = SubCategory.objects.get(
                id=subcategory_id)
        if budget_id:
            validated_data['budget'] = Budget.objects.get(id=budget_id)

        validated_data.pop('profile', None)
        return Transaction.objects.create(profile=profile, **validated_data)

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        subcategory_id = validated_data.pop('subcategory_id', None)
        budget_id = validated_data.pop('budget_id', None)

        if category_id is None:
            instance.category = None
        elif category_id:
            instance.category = Category.objects.get(id=category_id)

        if subcategory_id is None:
            instance.subcategory = None
        elif subcategory_id:
            instance.subcategory = SubCategory.objects.get(id=subcategory_id)

        if budget_id is None:
            instance.budget = None
        elif budget_id:
            instance.budget = Budget.objects.get(id=budget_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
