from rest_framework.viewsets import ModelViewSet

from .models import StorageCategory, StorageLocation
from .serializers import StorageSerializer, StorageCategorySerializer, StorageLocationSerializer


# TODO: we want only list/get from this ViewSet
class StorageViewSet(ModelViewSet):
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

    def get_queryset(self):
        queryset = StorageCategory.objects.all()
        queryset = queryset.get_cached_trees()
        return queryset


class StorageCategoryViewSet(ModelViewSet):
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
