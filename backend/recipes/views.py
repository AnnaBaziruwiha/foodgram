from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .filters import RecipeFilterSet
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsOwner, ReadOnly
from .serializers import (FavoriteSerializer, IngredientCreateSerializer, IngredientListSerializer,
                          IngredientAmountSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializers = {
        'default': RecipeSerializer,
        'create': RecipeCreateSerializer,
    }
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilterSet

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsOwner | IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializers = {
        'default': IngredientAmountSerializer,
        'create': IngredientCreateSerializer,
        'list': IngredientListSerializer,
        'retrieve':IngredientListSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


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
        serializer.save(user=self.request.user, recipe=recipe)


def download_shopping_cart(request):
    queryset = ShoppingCart.objects.filter(user=request.user).values(
        'recipe__amount__item__name',
        'recipe__amount__item__measurement_unit'
    ).annotate(
        Sum('recipe__amount__amount')
    )
    with open('shopping_cart.txt', 'w+') as cart_file:
        for item in queryset:
            name = item['recipe__amount__item__name']
            measurement_unit = item[
                'recipe__amount__item__measurement_unit'
            ]
            amount = item['recipe__amount__amount__sum']
            cart_file.write(
                f'{name} ({measurement_unit}) – {amount}'
            )
    return HttpResponse(cart_file, content_type='text/plain')


class FavoriteViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipes=recipe)
