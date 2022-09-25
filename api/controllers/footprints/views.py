from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers

from .models import FootprintCategory
from .serializers import FootprintCategorySerializer


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
