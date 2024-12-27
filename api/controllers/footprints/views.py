from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import mixins, parsers
from rest_framework.viewsets import GenericViewSet

from controllers.footprints.models import Footprint, FootprintCategory
from controllers.footprints.serializers import (
    FootprintCategorySerializer,
    FootprintCategoryTreeSerializer,
    FootprintSerializer,
)


@extend_schema(
    responses={200: OpenApiResponse(response=FootprintCategoryTreeSerializer)},
)
class TreeViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    Return a tree of footprints bundled into categories
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
    serializer_class = FootprintCategoryTreeSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = FootprintCategory.objects.all()
        return queryset


class FootprintCategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Footprints categories
    """

    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = FootprintCategorySerializer

    def get_queryset(self):
        queryset = FootprintCategory.objects.all()
        return queryset


class FootprintViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Footprints categories
    """

    anonymous_policy = True
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = FootprintSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id", None)

        queryset = Footprint.objects.all()

        if category_id:
            category = FootprintCategory.objects.get(id=category_id)

            if category is not None:
                queryset = queryset.filter(category=category)

        return queryset
