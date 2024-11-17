from rest_framework import serializers
from .models import Budget
from categories.serializers import CategorySerializer


class BudgetSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    category = CategorySerializer(read_only=True)  # To show category details
    category_id = serializers.IntegerField(write_only=True, required=False)  # Optional field to set category by ID

    class Meta:
        model = Budget
        fields = [
            'id',
            'profile',
            'name',
            'amount',
            'created_at',
            'updated_at',
            'category',
            'category_id',
        ]

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        profile = self.context['request'].user.profile  # Get the profile from the request context

        # Assign category if provided
        if category_id:
            validated_data['category_id'] = category_id

        # Remove 'profile' if it exists in validated_data to avoid duplication
        validated_data.pop('profile', None)

        # Explicitly set profile and pass the remaining data
        return Budget.objects.create(profile=profile, **validated_data)



    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)

        # Update category if provided
        if category_id is not None:
            instance.category_id = category_id

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
