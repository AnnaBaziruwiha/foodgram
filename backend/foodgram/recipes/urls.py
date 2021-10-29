from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (EditShoppingCartViewSet, FavoriteViewSet,
                    IngredientViewSet, RecipeViewSet, TagViewSet,
                    download_shopping_cart)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    EditShoppingCartViewSet,
    basename='add_to_shopping_cart'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorites'
)
urlpatterns = [
    path('', include(router.urls)),
    path(
        'download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    )
]
