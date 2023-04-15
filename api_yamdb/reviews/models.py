from django.contrib.auth.models import AbstractUser
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


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
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
        verbose_name='Слаг категории',
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.genre}: {self.title}'
