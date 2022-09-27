from .serializers import CreateCategorySerializer, CategorySerializer
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
    lookup_fields = ("id",)

    def get_serializer_class(self):
        if self.action == "list":
            return CategorySerializer
        else:
            return CreateCategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()

        # Do weird magic only for list (parts count, etc.)
        if self.action == "list":
            if self.request.auth:
                queryset = queryset.annotate(parts_count=Count("part"))
            else:
                queryset = queryset.annotate(
                    parts_count=Sum(Case(When(part__private=False, then=1), default=0, output_field=IntegerField()))
                )
            queryset = queryset.get_cached_trees()

        return queryset
