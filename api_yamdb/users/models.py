from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.constants import (ADMIN, EMAIL_MAX_LENGTH,
                                FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH,
                                MODERATOR, ROLE_MAX_LENGTH, USER, USER_ROLE,
                                USERNAME_MAX_LENGTH)
from .validators import validate_username


class ProjectUser(AbstractUser):
    username = models.CharField(
        verbose_name='Ник пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True
    )
    role = models.CharField(
        verbose_name='Права доступа',
        choices=USER_ROLE,
        default=USER,
        max_length=ROLE_MAX_LENGTH
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
