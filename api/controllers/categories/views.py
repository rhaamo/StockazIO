from .serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet
from .models import Category
from django.db.models import Count

# not sure about anonymous access for categories list
# maybe set the to-sell and public parts without categories sidebar
# and display the category in a sidebar, and do a group_by(category_id) ?


class CategoryViewSet(ModelViewSet):
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

    def get_queryset(self):
        queryset = Category.objects.all().annotate(parts_count=Count("part"))
        queryset = queryset.get_cached_trees()
        return queryset
