from django.contrib import admin

from .models import Ingredient, Recipe, Tag, ShoppingCart, Favorite


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'colored_name')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('favorited_count',)

    def favorited_count(self, obj):
        return obj.count_favorited()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('recipes',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('recipes',)
