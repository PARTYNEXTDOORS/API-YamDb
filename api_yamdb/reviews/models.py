from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES_CHOICES = [
    (ADMIN, 'Administrator'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
]


class User(AbstractUser):
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
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


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

    class Meta:
        ordering = ['-id']


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

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(
        max_length=50,
    )
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    description = models.TextField(
        max_length=256,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ['-id']


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
    text = models.CharField(max_length=256)
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

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique reviews'
            )]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(max_length=256)
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
    )

    class Meta:
        ordering = ['-id']
