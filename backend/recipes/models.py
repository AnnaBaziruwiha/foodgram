from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(verbose_name='Тэг', unique=True,
                            null=False, blank=False, max_length=200)
    color = models.CharField(
        unique=True, null=False, blank=False,
        max_length=7, default='#ffffff'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        null=False, blank=False
    )

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента', max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения', max_length=50
    )

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    name = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_amount'
    )
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name='ingredient_amount'
    )
    amount = models.IntegerField(
        verbose_name='Количество', validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ['name', 'recipe']


class Recipe(models.Model):
    name = models.CharField(verbose_name='Название рецепта', max_length=200)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount'
    )
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    image = models.ImageField(
        verbose_name='Картинка', upload_to='media/', blank=True, null=True
    )
    text = models.TextField(verbose_name='Текст рецепта')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления', validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    class Meta:
        unique_together = ['user', 'recipe']


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite'
    )

    class Meta:
        unique_together = ['user', 'recipe']
