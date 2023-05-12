from django.db.models.functions import Lower
from rest_framework.filters import OrderingFilter


class StoreOrdering(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        insensitive_ordering = getattr(view, 'ordering_case_insensitive_fields', ())

        if ordering:
            new_ordering = []
            for field in ordering:
                if field in insensitive_ordering:
                    new_ordering.append(Lower(field[1:]).desc() if field.startswith('-') else Lower(field).asc())
                else:
                    new_ordering.append(field)
            return queryset.order_by(*new_ordering)

        return queryset