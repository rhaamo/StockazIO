from .serializers import CategorySerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .models import Category
from django.db.models import Count, Sum, Case, When, IntegerField


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
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

    def get_queryset(self):
        if self.request.auth:
            queryset = Category.objects.all().annotate(parts_count=Count("part"))
        else:
            queryset = Category.objects.all().annotate(
                parts_count=Sum(Case(When(part__private=False, then=1), default=0, output_field=IntegerField()))
            )
        queryset = queryset.get_cached_trees()
        return queryset
