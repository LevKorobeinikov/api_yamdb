import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
