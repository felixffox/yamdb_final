from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Самостоятельная регистрация новых пользователей."""

    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = ("email", "username")
        model = User


class UsersByAdminSerializer(serializers.ModelSerializer):
    """Управление пользователями администратором."""

    role = serializers.ChoiceField(
        choices=["user", "moderator", "admin"], required=False
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
