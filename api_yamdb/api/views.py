from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Review, Title
from users.models import ProjectUser
from api.filters import TitleFilter
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModeratorOrReadOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitlePostSerializer, TitleSerializer,
    UserCreateSerializer, UserSerializer, UserTokenSerializer
)


class AdministratorViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Вьюсет для операций create/list/retrieve."""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""

    queryset = ProjectUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        user = get_object_or_404(ProjectUser, username=self.request.user)
        serializer = UserSerializer(user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateViewSet(APIView):
    """Вьюсет для регистрации."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTokenViewSet(APIView):
    """Вьюсет для токена."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(AdministratorViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AdministratorViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'],
                                 title_id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
