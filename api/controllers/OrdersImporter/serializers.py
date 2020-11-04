from rest_framework import serializers
from .models import Order, Item
from controllers.categories.serializers import CategorySerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=False)

    class Meta:
        model = Item
        fields = (
            "id",
            "vendor_part_number",
            "mfr_part_number",
            "manufacturer",
            "description",
            "quantity",
            "order",
            "category",
            "ignore",
        )


class OrderSerializer(WritableNestedModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items")
