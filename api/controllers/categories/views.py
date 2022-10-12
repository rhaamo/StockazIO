from collections import defaultdict

from django.db.models import Case, Count, IntegerField, Sum, When
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from controllers.categories.models import Category
from controllers.categories.serializers import CategorySerializer, CreateCategorySerializer


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

    def list(self, request, *args, **kwargs):
        """
        Return a nested json tree of the categories from the flat representation
        """
        children = defaultdict(list)
        for node in self.get_queryset():
            children[node.parent].append(node)

        def serialize(item, parent_id):
            d = {
                "id": item.id,
                "name": item.name,
                "parent": parent_id,
                "parts_count": item.parts_count,
                "children": [serialize(child, item.id) for child in children[item]],
            }
            return d

        roots = [serialize(root, None) for root in children[None]]

        return Response(roots, status=200)

    def get_queryset(self):
        # somehow the order_by is necessary even if the model still have ordering...
        queryset = Category.objects.with_tree_fields(False).select_related("parent").order_by("name")

        # Do weird magic only for list (parts count, etc.)
        if self.action == "list":
            if self.request.auth:
                queryset = queryset.annotate(parts_count=Count("part"))
            else:
                queryset = queryset.annotate(
                    parts_count=Sum(Case(When(part__private=False, then=1), default=0, output_field=IntegerField()))
                )

        return queryset
