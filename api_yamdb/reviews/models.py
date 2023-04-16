from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES_CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email адресс'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]


    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class Category(models.Model):
    name = models.CharField(
        max_length=50
    )
    slug = models.SlugField()


class Genre(models.Model):
    name = models.CharField(
        max_length=50
    )
    slug = models.SlugField()

class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг жанра',
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг категории',
    )

    def __str__(self):
        return self.name



class Title(models.Model):
    name = models.CharField(
        max_length=50,
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(max_length=200),
    score = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзывы',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='title',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
