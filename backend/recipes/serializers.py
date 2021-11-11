from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='name.id')
    name = serializers.ReadOnlyField(source='name.name')
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'measurement_unit', 'amount']


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ['id', 'amount']


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientAmount.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe_id=obj, user_id=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe_id=obj, user_id=request.user
        ).exists()

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart']


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ['id', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time', 'author', 'pub_date']

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть отрицательным'
            )
        return value

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        unique_ingredients = []
        if not ingredients:
            raise serializers.ValidationError('Не указаны ингредиенты')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    'Количество не может быть отрицательным'
                )
            if ingredient['id'] in unique_ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными'
                )
            else:
                unique_ingredients.append(ingredient['id'])
        return value

    def validate_tags(self, value):
        tags = self.initial_data.get('tags')
        if len(tags) > len(set(tags)):
            raise serializers.ValidationError('Теги не должны повторяться')
        return value

    def to_representation(self, instance):
        serializer = RecipeListSerializer(instance)
        return serializer.data

    def add_ingredients(self, ingredients, recipe):
        for item in ingredients:
            item_id = item['id']
            amount = item['amount']
            if IngredientAmount.objects.filter(recipe=recipe,
                                               name=item_id).exists():
                amount += F('amount')
            IngredientAmount.objects.update_or_create(
                recipe=recipe, name=item_id,
                defaults={'amount': amount}
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_ingredients(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(queryset=ShoppingCart.objects.all(),
                                    fields=['user', 'recipe'])
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(queryset=Favorite.objects.all(),
                                    fields=['user', 'recipe'])
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data
