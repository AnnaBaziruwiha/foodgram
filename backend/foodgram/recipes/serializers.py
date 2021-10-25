import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, image_string = data.split(';base64,')
            extension = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(image_string),
                name=id.urn[9:] + '.' + extension
            )
        return super(Base64ImageField, self).to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.measurement_unit = validated_data.get(
            'measurement_unit', instance.measurement_unit
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredients', 'tags', 'author',
                  'image', 'text', 'cooking_time', 'pub_date']
        optional_fields = ['tags', 'image']


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['user', 'ingredients']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    recipes = RecipeSerializer(many=True)

    class Meta:
        model = Favorite
        fields = ['user', 'recipes']
