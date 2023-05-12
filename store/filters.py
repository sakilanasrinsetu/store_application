import django_filters
from django_filters.rest_framework import FilterSet


from .models import Store


class StoreFilter(FilterSet):
    search_term = django_filters.CharFilter(label="search_term", method="filter_search_term")

    class Meta:
        model = Store
        fields = (
            "search_term",
        )

    def filter_search_term(self, objects, name, value):
        if value:
            queryset = Store.objects.filter(
                name__icontains=value
            )
            return queryset
        return None