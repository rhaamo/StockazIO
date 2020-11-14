from rest_framework.viewsets import ModelViewSet

from .models import FootprintCategory
from .serializers import FootprintCategorySerializer


class FootprintViewSet(ModelViewSet):
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

    def get_queryset(self):
        queryset = FootprintCategory.objects.all()
        return queryset
