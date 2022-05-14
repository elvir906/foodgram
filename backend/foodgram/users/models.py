from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            constraints.UniqueConstraint(
                fields=['user', 'author'],
                name='uniqueness of follow'
            ),
        )
