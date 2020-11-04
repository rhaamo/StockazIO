from rest_framework.viewsets import ModelViewSet

from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(ModelViewSet):
    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = OrderSerializer
    ordering_fields = ["date", "order_number", "status", "vendor", "import_state"]
    ordering = ["date"]

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset
