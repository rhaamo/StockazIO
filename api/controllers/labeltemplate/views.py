from rest_framework.viewsets import ModelViewSet

from .models import LabelTemplate
from .serializers import LabelTemplateSerializer


class LabelTemplateViewSet(ModelViewSet):
    """
    PDF Label Templates
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
    serializer_class = LabelTemplateSerializer

    def get_queryset(self):
        return LabelTemplate.objects.all()
