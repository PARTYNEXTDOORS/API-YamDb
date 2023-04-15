from rest_framework import serializers

from reviews.models import Title, Category, Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id')


class CategorySerializer(serializers.ModelSerializer):

    class Mets:
        model = Category
        exlude = ('id')


class TitleSerializer(serializers.ModelSerializer):
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
    genre = GenreSerializer(read_only=True,)
    category = CategorySerializer(read_only=True, many=True,)
    rating = serializers.ImageField(read_only=True,)

    class Meta:
        fields = '__all__'
        model = Title
