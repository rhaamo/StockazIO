from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers

from controllers.manufacturer.models import Manufacturer
from controllers.manufacturer.serializers import ManufacturersSerializer, ManufacturersCreateSerializer


class ManufacturersViewSet(ModelViewSet):
    """
    Manufacturer addresses
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

    def get_serializer_class(self):
        if self.action in ["create"]:
            return ManufacturersCreateSerializer
        else:
            return ManufacturersSerializer

    parse_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        return queryset
