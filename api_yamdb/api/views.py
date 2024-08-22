from django.db.models import Avg
from rest_framework import filters, mixins, status, viewsets

from reviews.models import Category, Genre, Title
from .filters import TitleFilter
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, TitlePostSerialzier)


class CategoryViewSet(None):  # AdminViewSet
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(None):  # AdminViewSet
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (None)  # IsAdminOrReadOnly,
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerialzier
        return TitleSerializer
