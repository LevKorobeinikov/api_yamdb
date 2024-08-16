from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserCreateViewSet, UserTokenViewSet, UserViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', UserCreateViewSet, basename='signup'),
    path('token/', UserTokenViewSet, basename='token')
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls))
]
