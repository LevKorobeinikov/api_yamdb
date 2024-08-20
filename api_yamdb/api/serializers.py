import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.validators import MinValueValidator, MaxValueValidator
from reviews.models import Comment, Review, Category, Genre, Title
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import (COD_MAX_LENGTH, EMAIL_MAX_LENGTH,
                                NO_USERNAMES, USERNAME_MAX_LENGTH, MIN_VALUE,
                                MAX_SCOPE_VALUE)
from users.models import ProjectUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=ProjectUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=ProjectUser.objects.all())]
    )

    class Meta:
        model = ProjectUser
        fields = '__all__'


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=ProjectUser.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=ProjectUser.objects.all())]
    )

    def validate_username(self, value):
        if value in NO_USERNAMES:
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        if ProjectUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с данным username уже существует'
            )
        return value

    def validate_email(self, value):
        if ProjectUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с данным email уже существует'
            )
        return value


class UsersMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=COD_MAX_LENGTH,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=MIN_VALUE,
                              message='Минимальная оценка - 1'),
            MaxValueValidator(limit_value=MAX_SCOPE_VALUE,
                              message='Максимальная оценка - 10')]
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=author,
                                     title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли рецензию'
                )
            return data

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
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
    rating = serializers.IntegerField(default=1)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',
                  )
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category',
                            )


class TitlePostSerialzier(serializers.ModelSerializer):
    """Cериализатор модели Title для изменения информации
    в ответе (response)."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        if (value > dt.date.today().year):
            raise serializers.ValidationError(
                'А вы оказывается из будущего'
            )
        return value

    def to_representation(self, instance):
        return TitleSerializer(instance).data
