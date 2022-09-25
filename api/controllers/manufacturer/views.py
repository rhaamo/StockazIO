from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers

from .models import Manufacturer
from .serializers import ManufacturersSerializer


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
    serializer_class = ManufacturersSerializer
    parse_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        return queryset
