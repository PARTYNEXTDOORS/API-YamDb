from django.urls import include, path
from rest_framework import routers

from .views import (GenreVewset, CategoryVewset, TitleVewset
                    UserViewSet, get_token, register)

router_v1 = routers.DefaultRouter()
router_v1.register('genre', GenreVewset, basename='genre')
router_v1.register('category', CategoryVewset, basename='category')
router_v1.register('title', TitleVewset, basename='title')
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
