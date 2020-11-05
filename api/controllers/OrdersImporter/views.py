from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework.response import Response

from .serializers import OrderSerializer, CategoryMatcherSerializer
from .models import CategoryMatcher, Order
from controllers.categories.models import Category
from .utils import rematch_orders


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


class CategoryMatcherViewSet(ModelViewSet):
    anonymous_policy = False
    required_scope = {
        "retrieve": "read",
        "create": "write",
        "destroy": "write",
        "update": "write",
        "partial_update": "write",
        "list": "read",
    }
    serializer_class = CategoryMatcherSerializer

    def get_queryset(self):
        queryset = CategoryMatcher.objects.all()
        return queryset


class CategoryMatcherBatchUpdater(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def patch(self, req):
        # Missing elements will be created
        new_items = []
        if len(req.data) <= 0:
            return Response({"detail": "Not found."}, 404)
        for item in req.data:
            if "id" in item:
                # Update
                db_item = CategoryMatcher.objects.get(id=item["id"])
                if db_item:
                    db_item.regexp = item["regexp"]
                    category = Category.objects.get(id=item["category"])
                    if not category:
                        continue
                    db_item.category = category
                    db_item.save()
            else:
                # Create
                category = Category.objects.get(id=item["category"])
                if not category:
                    continue
                db_item = CategoryMatcher(regexp=item["regexp"], category=category)
                db_item.save()
            new_items.append(db_item)
        serializer = CategoryMatcherSerializer(new_items, many=True)
        return Response(serializer.data, status=200)


class CategoryMatcherBatchRematcher(views.APIView):
    required_scope = "parts"
    anonymous_policy = False

    def get(self, req):
        # fetch orders
        orders = Order.objects.all().filter(import_state=1).prefetch_related("items")
        if not orders:
            return Response({"details": "ok"}, 200)

        # rematch
        rematch_orders(orders)

        return Response({"detail": "done"})
