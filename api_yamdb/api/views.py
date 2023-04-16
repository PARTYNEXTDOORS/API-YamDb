from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator


from rest_framework import permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrAuthenticated
from .serializers import (UserSerializer, TokenSerializer,
                          RegistrationSerializer, UserEditSerializer)
from .utils import confirmation_code_send_email
from reviews.models import User


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    user = User.objects.filter(username=request.data.get(
        'username'), email=request.data.get('email')).first()
    if user:
        confirmation_code_send_email(user)
        return Response({'email': user.email,
                         'username': user.username}, status=status.HTTP_200_OK)
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code_send_email(serializer.save())
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    http_method_names = ('get', 'patch', 'delete', 'post',)
    search_fields = ['=username']
    filter_backends = [SearchFilter]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrAuthenticated,)

    @action(methods=['get', 'patch',], detail=False, url_path='me',
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=UserEditSerializer,
            )
    def profile_users(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
