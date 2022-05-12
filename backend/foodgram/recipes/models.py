from django.contrib.auth import get_user_model

from django.db import models
from django.core.validators import MinValueValidator


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Ingredients(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название ингредиента'
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    measurement_unit = models.CharField(max_length=10, verbose_name='ед.изм.')

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}'


class Recipes(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    text = models.TextField(verbose_name='Рецепт приготовления')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name='Время приготовления'
    )
    tags = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes'
    )
    # image
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'
