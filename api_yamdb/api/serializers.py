from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from reviews.models import Review, Comments


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
