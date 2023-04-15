from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from rest_framework import filters, pagination, viewsets
from serializers import CategorySerializer, GenreSerializer
from serializers import TitleSerializer, TitleReadSerializer
from permissions import IsAdminOrReadOnly


class GenreVewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с Жанрами"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class CategoryVewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с Категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class TitleVewset(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с произведениями"""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer
