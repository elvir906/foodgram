from django.contrib.auth import get_user_model

from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import constraints


User = get_user_model()


class Tags(models.Model):
    ACID_GREEN = '#b0bf1a'
    AMETHYST = '#9966cc'
    AMBER = '#ffbf00'
    BRILLIANT_ROSE = '#ff55a3'
    FERRARI_RED = '#ff2800'

    COLORS_CHOICE = [
        (ACID_GREEN, 'Кислотно-зелёный'),
        (AMETHYST, 'Аметист'),
        (AMBER, 'Янтарь'),
        (BRILLIANT_ROSE, 'Бриллиантовая роза'),
        (FERRARI_RED, 'Красный Феррари'),
    ]

    name = models.CharField(max_length=150, unique=True,
                            verbose_name='название тэга')
    color = models.CharField(max_length=7, unique=True, choices=COLORS_CHOICE,
                             verbose_name='HEX код цвета')
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='Название ингредиента'
    )
    unit = models.CharField(max_length=10, verbose_name='ед.изм.')

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            constraints.UniqueConstraint(
                fields=['name',  'unit'],
                name='uniqueness of food and measurement unit'
            ),
        )

    def __str__(self):
        return self.name


class Recipes(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    text = models.TextField(verbose_name='Рецепт приготовления (описание)')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Минимальное вемя приготовления - 1 (одна) минута'
            )
        ],
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Поле тэгов',
    )
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Фото блюда')
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Необходимые ингредиенты',
        related_name='recipes',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                 1, message='Минимальное количество ингредиента д.б. 1'
            ),
        ],
        verbose_name='Количество'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='recipe`s ingredient uniqueness')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            constraints.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniqueness of user and favorite recipes'
            ),
        )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = (
            constraints.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniqueness of user and foods in cart'
            ),
        )
