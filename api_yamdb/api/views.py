<<<<<<< HEAD
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import ProjectUser
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (
    UserSerializer, UserCreateSerializer, UserTokenSerializer
)


class AdministratorViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+\Z)',
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(ProjectUser, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid()
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = UserCreateSerializer
    permissions_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if serializer.is_valid() or ProjectUser.objects.filter(
            usrname=username, email=email
        ).exists():
            user, __ = ProjectUser.objects.get_or_create(
                username=username, email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Код подтверждения',
                message=f'Код подтверждения: {confirmation_code}',
                from_email='yamdb@yamdb.com',
                recipient_list=(email,),
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_data')
        user = get_object_or_404(ProjectUser, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения неверный'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 4980483 (готовы необходимые модели для начала работы)
