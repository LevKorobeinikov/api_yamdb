from django.urls import include, path

from .views import UserViewSet


router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/', include('users.urls'))
]
