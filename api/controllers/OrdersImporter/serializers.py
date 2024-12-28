from drf_spectacular.utils import extend_schema_field

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from controllers.categories.serializers import SingleCategorySerializer
from controllers.distributor.serializers import DistributorsSerializer
from controllers.footprints.serializers import FootprintSerializer
from controllers.manufacturer.serializers import ManufacturersSerializer
from controllers.OrdersImporter.models import CategoryMatcher, Item, Order
from controllers.part.serializers import PartSerializer


class ItemSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)
    manufacturer_db = ManufacturersSerializer(many=False, read_only=True)
    footprint_db = FootprintSerializer(many=False, read_only=True)
    part_db = PartSerializer(many=False, read_only=False)

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
            "footprint_db",
            "part_db",
            "new_in_stock",
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
            "category",
            "ignore",
            "manufacturer_db",
            "footprint_db",
            "part_db",
            "new_in_stock",
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
    items = ItemCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ("id", "date", "order_number", "status", "vendor", "import_state", "items", "vendor_db")


class CategoryMatcherCreateSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=True)

    class Meta:
        model = CategoryMatcher
        fields = ("id", "regexp", "category")


class CategoryMatcherSerializer(serializers.ModelSerializer):
    category = SingleCategorySerializer(many=False, read_only=False)

    class Meta:
        model = CategoryMatcher
        fields = ("id", "regexp", "category")
