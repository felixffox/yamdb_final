from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.views import MeViewSet, SignUpViewSet, TokenViewSet, UserViewSet

app_name = "api"

router = SimpleRouter()
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")
router.register("titles", TitleViewSet, basename="title")

router.register(r"users", UserViewSet)
router.register(r"auth/signup", SignUpViewSet)
router.register(r"auth/token", TokenViewSet)

urlpatterns = [
    path(
        "v1/users/me/",
        MeViewSet.as_view(
            {
                "get": "get_me",
                "patch": "patch_me",
            }
        ),
        name="me-by-username",
    ),
    path(
        "v1/users/<str:username>/",
        UserViewSet.as_view(
            {
                "get": "get_by_username",
                "patch": "patch_by_username",
                "delete": "delete_by_username",
            }
        ),
        name="user-by-username",
    ),
    path("v1/", include(router.urls)),
]
