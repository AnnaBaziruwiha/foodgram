from django.contrib.auth.hashers import make_password
from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import CustomUser, Subscription


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
        ]

    def validate_password(self, value):
        return make_password(value)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['author', 'user']
