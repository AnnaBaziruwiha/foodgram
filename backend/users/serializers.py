from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser, Subscription
from recipes.models import Recipe


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            author__id=obj.id, user__id=request.user.id
        ).exists()

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        ]


class CustomUserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class CustomUserListSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:(int(recipes_limit))]
        context = {'request': request}
        return CustomUserRecipeSerializer(
            recipes, many=True, context=context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta(CustomUserSerializer.Meta):
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Subscription
        fields = ['author', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['author', 'user'])
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return CustomUserListSerializer(
            instance.author, context=context
        ).data
