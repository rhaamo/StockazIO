from .serializers import CategorySerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Category
from django.db.models import Count, Sum, Case, When, IntegerField

# not sure about anonymous access for categories list
# maybe set the to-sell and public parts without categories sidebar
# and display the category in a sidebar, and do a group_by(category_id) ?


class CategoryViewSet(ReadOnlyModelViewSet):
    """
    Retrieve Categories Tree
    """

    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": None,
    }
    serializer_class = CategorySerializer
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.auth:
            queryset = Category.objects.all().annotate(parts_count=Count("part"))
        else:
            queryset = Category.objects.all().annotate(
                parts_count=Sum(Case(When(part__private=False, then=1), default=0, output_field=IntegerField()))
            )
        queryset = queryset.get_cached_trees()
        return queryset
