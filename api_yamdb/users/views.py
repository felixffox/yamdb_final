from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import RoleAdmin
from .serializers import UserSerializer
from .serializers import UsersByAdminSerializer


class MeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Me."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_me(self, request):
        """Выдаем Me."""
        return Response(
            UsersByAdminSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    def patch_me(self, request):
        """Патчим Me."""
        instance = request.user
        serializer = UsersByAdminSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(role=instance.role)
            return Response(
                UsersByAdminSerializer(instance).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Самостоятельная регистрация новых пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def send_confirmation_code(self, request):
        """После сохранения отправляем по почте confirmation_code."""
        email = request.data.get("email")
        confirmation_code = request.data.get("confirmation_code")
        username = request.data.get("confirmation_code")
        email2send = EmailMessage(
            f"confirmation_code for user {username}",
            str(confirmation_code),
            email,
            [email],
        )
        email2send.send()

    def create(self, request, *args, **kwargs):
        """Самостоятельная регистрация новых пользователей."""
        username = request.data.get("username")
        email = request.data.get("email")
        if username == "me":
            return Response(
                {"error": "username=me is depricated"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(username=username).first()
        if user:
            if email != user.email:
                return Response(
                    {"error": "incorrect email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.send_confirmation_code(request)
            return Response(
                {"email": user.email, "username": user.username},
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.send_confirmation_code(request)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Токен."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            return Response(
                ["username is required field."],
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(username=username).first()
        if not user:
            return Response(
                ["incorrect username."],
                status=status.HTTP_404_NOT_FOUND,
            )
        confirmation_code = request.data.get("confirmation_code")
        if not confirmation_code:
            return Response(
                ["confirmation_code is required."],
                status=status.HTTP_403_FORBIDDEN,
            )
        if str(confirmation_code) != str(user.confirmation_code):
            return Response(
                ["Incorrect confirmation_code"],
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token),
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями администратором."""

    queryset = User.objects.all()
    serializer_class = UsersByAdminSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [RoleAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    def create(self, request, *args, **kwargs):
        """Создаем пользователя."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_by_username(self, request, username):
        """Выдаем пользователя не по pk, а по имени."""
        user = get_object_or_404(User, username=username)
        return Response(
            UsersByAdminSerializer(user).data, status=status.HTTP_200_OK
        )

    def patch_by_username(self, request, username):
        """Патчим пользователя не по pk, а по имени."""
        instance = get_object_or_404(User, username=username)
        serializer = UsersByAdminSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete_by_username(self, request, username):
        """Удаляем пользователя не по pk, а по имени."""
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(
            {"result": "user is deleted"}, status=status.HTTP_204_NO_CONTENT
        )
