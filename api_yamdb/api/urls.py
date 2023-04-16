from django.urls import include, path
from rest_framework import routers

from .views import (GenreVewset, CategoryVewset, TitleVewset)

router_v1 = routers.DefaultRouter()
router_v1.register('genre', GenreVewset, basename='genre')
router_v1.register('category', CategoryVewset, basename='category')
router_v1.register('title', TitleVewset, basename='title')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
