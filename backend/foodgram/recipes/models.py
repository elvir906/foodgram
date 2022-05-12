from django.contrib.auth import get_user_model

from django.db import models
from django.core.validators import MinValueValidator


User = get_user_model()


class Recipes(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    text = models.TextField(verbose_name='Рецепт приготовления')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name='Время приготовления'
    )
    # tags
    # image
    # ingredients


class Ingredients(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название ингредиента'
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    measurement_unit = models.CharField(max_length=5, verbose_name='ед.изм.')
