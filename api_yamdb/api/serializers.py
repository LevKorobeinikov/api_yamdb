from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from reviews.models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    score = serializers.IntegerField(
        validators=[MinValueValidator(
            settings.MIN_VALUE), MaxValueValidator(settings.MAX_SCOPE_VALUE)]
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pubdate']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='unique_author_title'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method != 'POST':
            return data
        author = request.user
        title_id = self.context.get('view', {}).kwargs.get('title_id')
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли рецензию'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'text', 'author', 'pubdate']
