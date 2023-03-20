from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name="Категория"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанры."""

    name = models.CharField(
        max_length=256,
        verbose_name="Жанр"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name="Произведение"
    )
    year = models.IntegerField()
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        through="GenreTitle"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        related_name="title",
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("id",)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связующая модель для поля жанра и произведения."""

    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(models.Model):
    """Модель отзыва"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(
        max_length=2500
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор"
    )
    score = models.IntegerField(
        "оценка",
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={"validators": "Оценка от 1 до 10!"},
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"),
                name="unique_review")
        ]
        ordering = ("pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария"""

    rewiew = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв"
    )
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
