import django_filters
from reviews.models import Title


class TitlesFilter(django_filters.FilterSet):
    """Фильтр для эндпоинта /api/v1/titles/ который даёт возможность
    фильтровать по slug полю, имени и году"""

    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="contains"
    )
    genre = django_filters.CharFilter(
        field_name="genre__slug",
        lookup_expr="contains"
    )
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="contains"
    )
    year = django_filters.NumberFilter(
        field_name="year",
        lookup_expr="contains"
    )

    class Meta:
        model = Title
        fields = "__all__"
