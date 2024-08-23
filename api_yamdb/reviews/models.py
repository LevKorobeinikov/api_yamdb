from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from users.models import ProjectUser
from reviews.utilites import current_year


class AbstractModelCategoryGenre(models.Model):
    name = models.CharField('Имя', max_length=settings.LIMIT_NAME_TEXT)
    slug = models.SlugField(
        'Slug', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class AbstractModelReviewComment(models.Model):
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        ProjectUser, on_delete=models.CASCADE,
        verbose_name='Aвтор')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:settings.LIMIT_NAME_TEXT]


class Category(AbstractModelCategoryGenre):
    class Meta(AbstractModelCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractModelCategoryGenre):
    class Meta(AbstractModelCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        'Название произведения', max_length=settings.LIMIT_NAME_TEXT)
    year = models.SmallIntegerField(
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
        Genre, through='GenreTitle',)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title',
            ),
        )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(AbstractModelReviewComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение')
    score = models.PositiveSmallIntegerField('Оценка', db_index=True,)

    class Meta(AbstractModelReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(AbstractModelReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(AbstractModelReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
