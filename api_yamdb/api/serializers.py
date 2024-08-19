import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from reviews.models import Review, Comments, Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(limit_value=settings.MIN_VALUE,
                              message='Минимальная оценка - 1'),
            MaxValueValidator(limit_value=settings.MAX_SCOPE_VALUE,
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
        model = Comments
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
