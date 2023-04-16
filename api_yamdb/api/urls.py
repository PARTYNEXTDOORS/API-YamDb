from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, get_token, register

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', register, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
