from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import StorageCategory, StorageLocation
from .serializers import StorageSerializer, StorageCategorySerializer, StorageLocationSerializer


@extend_schema(parameters=[OpenApiParameter("id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)])
class StorageViewSet(ModelViewSet):
    """
    Storage tree
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
    serializer_class = StorageSerializer
    # we want only get and list
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = StorageCategory.objects.all()
        queryset = queryset.get_cached_trees()
        return queryset


class StorageCategoryViewSet(ModelViewSet):
    """
    Storage categories
    """

    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = StorageCategorySerializer

    def get_queryset(self):
        return StorageCategory.objects.all()


class StorageLocationViewSet(ModelViewSet):
    """
    Storage locations
    """

    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = StorageLocationSerializer

    def get_queryset(self):
        return StorageLocation.objects.all()
