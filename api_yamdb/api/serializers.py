from rest_framework import serializers

import datetime

from reviews.models import Title, Category, Genre, User, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Жанров"""
    class Meta:
        model = Genre
        exlude = 'id'
        fields = ('__all__')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Категорий"""
    class Meta:
        model = Category
        exlude = 'id'
        fields = ('__all__')


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
        fields = '__all__'


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
            raise serializers.ValidationError(
                'Проверьте год выпука!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmations_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username',)
        model = User

    def validate_username(self, name):
        if name.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя "me".'
            )
        return name
