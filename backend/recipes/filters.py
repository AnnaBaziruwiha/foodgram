from django_filters import rest_framework as filters

from .models import Ingredient, Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        lookup_expr='contains',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(method='get_shopping_cart')
    is_favorited = filters.BooleanFilter(method='get_favorite')

    def get_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return Recipe.objects.all()

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorite__user=self.request.user)
        return Recipe.objects.all()

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']
