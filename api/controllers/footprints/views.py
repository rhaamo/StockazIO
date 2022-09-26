from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import parsers, mixins
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import FootprintCategory
from .serializers import FootprintCategorySerializer


# Rework:
# Main View = Footprint
# / = with categories
# but post etc. should be all
# if not possible
# then add a /tree with FootprintCategory.objects.all() as get only
# Sub view /categories/ FootprintCategory


@extend_schema(
    responses={
        200: OpenApiResponse(
            response=FootprintCategorySerializer
        )
    },
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
    serializer_class = FootprintCategorySerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = FootprintCategory.objects.all()
        return queryset


class FootprintViewSet(ModelViewSet):
    """
    Footprints types
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
    serializer_class = FootprintCategorySerializer
    parse_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        queryset = FootprintCategory.objects.all()
        return queryset
