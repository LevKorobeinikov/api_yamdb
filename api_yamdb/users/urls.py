from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    UserCreateViewSet, UserTokenViewSet, UserViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet, name='signup'),
    path('v1/auth/token/', UserTokenViewSet, name='token')
]
