from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model

from reviews.utilites import current_year

User = get_user_model()


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
        default_related_name = "titles"  # do I need to specify my related_name? TODO


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Title')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(  # TODO
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Aвтор')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        db_index=True,
        validators=[MinValueValidator(
            limit_value=settings.MIN_VALUE,
            message='Минимальная оценка - 1'),
            MaxValueValidator(
            limit_value=settings.MAX_SCOPE_VALUE,
            message='Максимальная оценка - 10')])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return f'Рецензия от {self.author} на {self.title}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Рецензия'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(  # TODO
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Комментарий от {self.author} на {self.review}'
