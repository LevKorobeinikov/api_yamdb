from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import (COD_MAX_LENGTH, EMAIL_MAX_LENGTH,
                                NO_USERNAMES, USERNAME_MAX_LENGTH)
from users.models import ProjectUser


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = ProjectUser
        fields = '__all__'


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value in NO_USERNAMES:
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с данным username уже существует'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с данным email уже существует'
            )
        return value


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=COD_MAX_LENGTH,
        required=True
    )
