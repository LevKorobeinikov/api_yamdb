from django.urls import include, path

urlpatterns = [
    path('v1/auth/', include('users.urls'))
]
