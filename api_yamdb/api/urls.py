from rest_framework import routers
from django.urls import path, include

from .views import (GenreVewset, CategoryVewset, TitleVewset,
                    ReviewViewSet, CommentViewSet,
                    UserViewSet, get_token, register)

router_v1 = routers.DefaultRouter()
router_v1.register('genres', GenreVewset, basename='genre')
router_v1.register('categorys', CategoryVewset, basename='category')
router_v1.register('titles', TitleVewset, basename='title')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'title/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
