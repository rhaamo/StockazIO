from rest_framework.viewsets import ModelViewSet

from .models import StorageCategory
from .serializers import StorageSerializer


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
