from django.urls import path

from api.views import (
    UserCreateViewSet, UserTokenViewSet
)


urlpatterns = [
    path('signup/', UserCreateViewSet, name='signup'),
    path('token/', UserTokenViewSet, name='token')
]
