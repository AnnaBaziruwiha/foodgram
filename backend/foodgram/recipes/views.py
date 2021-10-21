from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .filters import RecipeFilterSet
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsOwner, NoObjectPermission, ReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        (IsAuthenticatedOrReadOnly & NoObjectPermission) | IsAdminUser
    ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilterSet

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminUser | IsOwner]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class EditShoppingCartViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, ingredients=recipe.ingredients)


def download_shopping_cart(request):
    shopping_cart = get_object_or_404(ShoppingCart, user=request.user)
    ingredients = shopping_cart.ingredients.all()
    # here i must create the file and then output it
    return HttpResponse(content_type='application/pdf')


class FavoriteViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipes=recipe.ingredients)
