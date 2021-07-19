from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    bio = models.TextField(verbose_name='Биография', null=True, blank=True)
    REQUIRED_FIELDS = ['email']
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    class Meta:
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role in (UserRole.ADMIN, UserRole.MODERATOR)


class Category(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Имя произведения',
        max_length=100, db_index=True)
    description = models.TextField(verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год', db_index=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', db_index=True)
    category = models.ForeignKey(
        Category, related_name='titles', verbose_name='Категория',
        on_delete=models.SET_NULL, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Произведение'


class Review(models.Model):
    title = models.ForeignKey(
        Title, verbose_name='Произведение',
        related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст ревью')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        related_name='reviews', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Ревью'
        unique_together = ['title', 'author']


class Comment(models.Model):
    review = models.ForeignKey(
        Review, verbose_name='Ревью',
        related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        related_name='comments', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        verbose_name='Дата рубликации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
