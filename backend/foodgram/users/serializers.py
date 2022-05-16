from django.contrib.auth import get_user_model

from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Follow

User = get_user_model()


class UsresCustomSerializer(UserSerializer):
    is_subscriber = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscriber'
        )

    def get_is_subscriber(self, obj):
        user = self.context.get('request').user
        if user.is_anonymus:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class UsersCustomCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name'
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
