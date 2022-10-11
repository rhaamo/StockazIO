from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.response import Response

from controllers.storage.models import Storage
from controllers.storage.serializers import StorageSerializer
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
                "children": [serialize(child) for child in children[parent]],
            }
            if parent.picture:
                d["picture"] = request.build_absolute_uri(parent.picture.url)
                d["picture_medium"] = request.build_absolute_uri(parent.picture_medium.url)
            return d

        roots = [serialize(root) for root in children[None]]

        return Response(roots, status=200)

    def get_queryset(self):
        queryset = Storage.objects.all()
        return queryset
