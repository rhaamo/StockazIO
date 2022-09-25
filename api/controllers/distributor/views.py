from rest_framework.viewsets import ModelViewSet

from .models import Distributor
from .serializers import DistributorsSerializer


class DistributorsViewSet(ModelViewSet):
    """
    Distributor addresses
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
    serializer_class = DistributorsSerializer

    def get_queryset(self):
        queryset = Distributor.objects.all()
        return queryset
