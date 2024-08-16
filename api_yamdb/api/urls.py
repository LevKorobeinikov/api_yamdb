from django.urls import include, path
from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$',
                ReviewViewSet, basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)/$',  # noqa
    CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),
]