from django.urls import path

from api.views import (
    UserCreateViewSet, UserTokenViewSet
)


urlpatterns = [
    path('signup/', UserCreateViewSet.as_view(), name='signup'),
    path('token/', UserTokenViewSet.as_view(), name='token')
]
