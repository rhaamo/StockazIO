from rest_framework import serializers
from .models import Order, Item, CategoryMatcher
from controllers.categories.serializers import SingleCategorySerializer
from controllers.distributor.serializers import DistributorsSerializer
from controllers.manufacturer.serializers import ManufacturersSerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_spectacular.utils import extend_schema_field


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


class OrderListSerializer(WritableNestedModelSerializer):
    vendor_db = DistributorsSerializer(many=False, read_only=True)
    items_count = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_items_count(self, obj):
        return obj.items_count

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items_count", "vendor_db")


class OrderCreateSerializer(WritableNestedModelSerializer):
    # items = ItemCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        # fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items", "vendor_db")
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "vendor_db")


class CategoryMatcherSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)

    class Meta:
        model = CategoryMatcher
        fields = ("id", "regexp", "category")
