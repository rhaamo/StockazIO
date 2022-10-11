from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.response import Response

from controllers.storage.models import StorageCategory, StorageLocation, Storage
from controllers.storage.serializers import StorageSerializer, StorageCategorySerializer, StorageLocationSerializer
from collections import defaultdict

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

    def list(self, request, *args, **kwargs):
        """
        Return a nested json tree of the storages from the flat representation
        """
        children = defaultdict(list)
        for node in Storage.objects.with_tree_fields(False).select_related("parent"):
            children[node.parent].append(node)

        def serialize(parent):
            d = {
                "id": parent.id,
                "name": parent.name,
                "uuid": parent.uuid,
                "description": parent.description,
                "children": [serialize(child) for child in children[parent]]
            }
            if parent.picture:
                d["picture"] = parent.picture.url
                d["picture_medium"] = parent.picture_medium.url
            return d

        roots = [serialize(root) for root in children[None]]

        return Response(roots, status=200)

    def get_queryset(self):
        queryset = Storage.objects.all()
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
