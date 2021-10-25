from django.db import models
from django.utils.html import format_html

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default='#ffffff')
    slug = models.SlugField(max_length=50)

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.color
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)
    quantity = models.FloatField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipe'
    )
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        verbose_name='Картинка', upload_to='recipes/', blank=True, null=True
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']

    def count_favorited(self):
        return Favorite.objects.filter(recipes__id=self.id).count()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='shopping'
    )
    ingredients = models.ManyToManyField(Ingredient)


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='favorite'
    )
    recipes = models.ManyToManyField(Recipe)
