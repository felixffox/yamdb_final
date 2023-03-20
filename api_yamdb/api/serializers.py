from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != "POST":
            return data
        author = request.user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializerGET(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET запросе."""

    genre = GenreSerializer(Genre.objects.all(), many=True)
    category = CategorySerializer(Category.objects.all())
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при остальных запросах."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = "__all__"
