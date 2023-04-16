from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import filters, pagination, permissions, status, viewsets
from reviews.models import Category, Genre, Title, User, Review
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdminOrReadOnly, IsAdminOrAuthenticated
from .mixins import ModelMixinSet
from .utils import confirmation_code_send_email
from .filters import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleReadSerializer,
                          UserSerializer, TokenSerializer,
                          RegistrationSerializer, UserEditSerializer,
                          CommentSerializer, ReviewSerializer)


class GenreVewset(ModelMixinSet):
    """Вьюсет для работы с Жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryVewset(ModelMixinSet):
    """Вьюсет для работы с Категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleVewset(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями"""
    queryset = Title.objects.order_by('id').annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleCreateSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer = serializer.save(
            author=self.request.user,
            review=review
        )
        return serializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer = serializer.save(
            author=self.request.user,
            title=title
        )
        return serializer
