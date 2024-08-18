from django.urls import path

from api.views import (
    UserCreateViewSet, UserTokenViewSet
)


urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet, name='signup'),
    path('v1/auth/token/', UserTokenViewSet, name='token')
]
