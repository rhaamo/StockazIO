from rest_framework import serializers
from .models import Order, Item, CategoryMatcher
from controllers.categories.serializers import SingleCategorySerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)

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
    item_set = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "item_set")


class CategoryMatcherSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)

    class Meta:
        model = CategoryMatcher
        fields = ("id", "regexp", "category")
