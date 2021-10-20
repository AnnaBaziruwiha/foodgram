from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Subscription, User


class BaseUserRegistrationSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['author', 'user']
