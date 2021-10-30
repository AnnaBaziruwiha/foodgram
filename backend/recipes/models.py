from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=7, default='#ffffff'
    )
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    item = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amount'
    )
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name='amount'
    )
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['item', 'recipe']


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipe'
    )
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        verbose_name='Картинка', upload_to='media/', blank=True, null=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='shopping'
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
        Recipe, on_delete=models.CASCADE, related_name='favorited'
    )

    class Meta:
        unique_together = ['user', 'recipe']
