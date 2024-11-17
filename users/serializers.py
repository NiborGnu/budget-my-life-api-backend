from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator, ValidationError


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    username = serializers.CharField(
        source='owner.username',
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                message="This username is already taken.")
            ],
    )
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            return request.user == obj.owner
        return False

    class Meta:
        model = Profile
        fields = [
            'id',
            'owner',
            'username',
            'created_at',
            'updated_at',
            'first_name',
            'last_name',
            'is_owner',
        ]

    def validate(self, data):
        user_data = data.get('owner', {})
        username = user_data.get('username')

        # Validate username length
        if username and len(username) < 3:
            raise ValidationError(
                {"username": "Username must be at least 3 characters long."}
            )

        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('owner', {})
        username = user_data.get('username')

        # Update username only if provided
        if username and username != instance.owner.username:
            instance.owner.username = username
            instance.owner.save()

        # Update other fields in the Profile model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user