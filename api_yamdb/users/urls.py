from django.urls import include, path
from rest_framework import routers

from .views import MeViewSet, UsersByAdminViewSet, UserViewSet, token

user_create = UserViewSet.as_view({"post": "create"})
by_username = UsersByAdminViewSet.as_view(
    {
        "get": "get_by_username",
        "patch": "patch_by_username",
        "delete": "delete_by_username",
    }
)

me_username = MeViewSet.as_view(
    {
        "get": "get_me",
        "patch": "patch_me",
    }
)
router = routers.SimpleRouter()
router.register(r"users", UsersByAdminViewSet)

urlpatterns = [
    path("signup/", user_create, name="user-create"),
    path("token/", token, name="token"),
    path(
        "users/me/",
        me_username,
        name="me-username",
    ),
    path(
        "users/<str:username>/",
        by_username,
        name="by-username",
    ),
    path("", include(router.urls)),
]
