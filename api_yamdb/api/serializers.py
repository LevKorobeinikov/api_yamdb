import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb.constants import (
    COD_MAX_LENGTH, EMAIL_MAX_LENGTH,
    MAX_SCOPE_VALUE, MIN_VALUE,
    NO_USERNAMES, USERNAME_MAX_LENGTH
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ProjectUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = ProjectUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
    )

    def validate_username(self, value):
        if value in NO_USERNAMES:
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        return value


class UsersMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=COD_MAX_LENGTH,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=MIN_VALUE,
                message=f'Минимальная оценка - {MIN_VALUE}'),
            MaxValueValidator(
                limit_value=MAX_SCOPE_VALUE,
                message=f'Максимальная оценка - {MAX_SCOPE_VALUE}')]
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=author,
                                 title_id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли рецензию'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=1, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',
                  )
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category',
                            )


class TitlePostSerializer(serializers.ModelSerializer):
    """Cериализатор модели Title для изменения информации
    в ответе (response)."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        if (value > dt.date.today().year):
            raise serializers.ValidationError(
                'А вы оказывается из будущего'
            )
        return value

    def to_representation(self, instance):
        return TitleSerializer(instance).data
