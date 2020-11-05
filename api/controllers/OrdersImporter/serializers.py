from rest_framework import serializers
from .models import Order, Item, CategoryMatcher
from controllers.categories.serializers import SingleCategorySerializer
from controllers.distributor.serializers import DistributorsSerializer
from controllers.manufacturer.serializers import ManufacturersSerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)
    manufacturer_db = ManufacturersSerializer(many=False, read_only=True)

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
            "manufacturer_db",
        )


class ItemCreateSerializer(serializers.ModelSerializer):
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
            "manufacturer_db",
        )


class OrderSerializer(WritableNestedModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    vendor_db = DistributorsSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items", "vendor_db")


class OrderCreateSerializer(WritableNestedModelSerializer):
    items = ItemCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items", "vendor_db")


class CategoryMatcherSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)

    class Meta:
        model = CategoryMatcher
        fields = ("id", "regexp", "category")
