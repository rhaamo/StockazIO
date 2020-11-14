from rest_framework.viewsets import ModelViewSet

from .models import Manufacturer
from .serializers import ManufacturersSerializer


class ManufacturersViewSet(ModelViewSet):
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

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        return queryset
