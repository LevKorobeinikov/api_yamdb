import datetime as dt

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.constants import (
    CHECK_USERNAME, COD_MAX_LENGTH, EMAIL_MAX_LENGTH,
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
        regex=CHECK_USERNAME,
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
    )

    class Meta:
        model = ProjectUser
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == NO_USERNAMES:
            raise serializers.ValidationError(
                f'Использовать имя {value} в качестве username запрещено'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (ProjectUser.objects.filter(username=username).exists()
                and not ProjectUser.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                f'Пользователь со значением username = {username}'
                'уже существует'
            )
        if (ProjectUser.objects.filter(email=email).exists()
                and not ProjectUser.objects.filter(username=username)
                .exists()):
            raise serializers.ValidationError(
                f'Пользователь со значением email = {email}'
                'уже существует'
            )
        return super().validate(data)

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        user, _ = ProjectUser.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(email,),
            fail_silently=True,
        )
        return user


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=COD_MAX_LENGTH,
        required=True,
    )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(ProjectUser, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
        return super().validate(data)


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
    rating = serializers.IntegerField(default=0, read_only=True)

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
