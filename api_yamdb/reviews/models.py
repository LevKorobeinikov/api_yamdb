from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.utilites import current_year


class AbstractModelCategoryGenre(models.Model):
    name = models.CharField('Имя', max_length=settings.LIMIT_NAME_TEXT)
    slug = models.SlugField(
        'Slug', unique=True, max_length=settings.LIMIT_SLUG)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(AbstractModelCategoryGenre):
    class Meta(AbstractModelCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = "categories"


class Genre(AbstractModelCategoryGenre):
    class Meta(AbstractModelCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = "genres"


class Title(models.Model):
    name = models.CharField(
        'Название произведения', max_length=settings.LIMIT_NAME_TEXT)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[MinValueValidator(
                    limit_value=settings.MIN_VALUE,
                    message='Нулевой год ставить недопустимо'),
                    MaxValueValidator(
                    limit_value=current_year,
                    message='А вы оказывается из будущего')])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
        default_related_name = "titles"
