from rest_framework import serializers
import datetime

from reviews.models import Title, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Жанров"""
    class Meta:
        model = Genre
        exlude = 'id'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Категорий"""
    class Mets:
        model = Category
        exlude = 'id'


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для Произведений(Create)"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fileds = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для Произведений(Read)"""
    genre = GenreSerializer(read_only=True, many=True,)
    category = CategorySerializer(read_only=True,)
    rating = serializers.ImageField(read_only=True,)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпука!')
        return value
