from rest_framework import serializers
from .models import ParametersUnit, PartUnit, Part, PartParameter, PartAttachment

from controllers.storage.serializers import StorageLocationSerializer
from controllers.categories.serializers import SingleCategorySerializer
from controllers.footprints.serializers import FootprintSerializer
from controllers.distributor.serializers import DistributorSkuSerializer
from controllers.manufacturer.serializers import PartManufacturerSerializer


class ParametersUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametersUnit
        fields = ("id", "name", "symbol", "prefix", "description")


class PartsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnit
        fields = ("id", "name", "short_name", "description")


class PartSerializer(serializers.ModelSerializer):
    storage = StorageLocationSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)

    class Meta:
        model = Part
        fields = (
            "id",
            "name",
            "description",
            "stock_qty",
            "stock_qty_min",
            "status",
            "needs_review",
            "condition",
            "can_be_sold",
            "private",
            "internal_part_number",
            "part_unit",
            "category",
            "storage",
            "footprint",
            "uuid",
            "comment",
            "production_remarks",
        )


class PartCreateSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = (
            "id",
            "name",
            "description",
            "stock_qty",
            "stock_qty_min",
            "status",
            "needs_review",
            "condition",
            "can_be_sold",
            "private",
            "internal_part_number",
            "part_unit",
            "category",
            "storage",
            "footprint",
            "uuid",
            "comment",
            "production_remarks",
        )


class PartParameterSerializer(serializers.ModelSerializer):
    unit = ParametersUnitSerializer(many=False, read_only=True)

    class Meta:
        model = PartParameter
        fields = ("id", "name", "description", "value", "unit")


class PartAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartAttachment
        fields = ("id", "description", "file")


class PartRetrieveSerializer(serializers.ModelSerializer):
    storage = StorageLocationSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)
    part_parameters_value = PartParameterSerializer(many=True, read_only=True)
    distributors_sku = DistributorSkuSerializer(many=True, read_only=True)
    manufacturers_sku = PartManufacturerSerializer(many=True, read_only=True)
    part_attachments = PartAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Part
        fields = (
            "id",
            "name",
            "description",
            "stock_qty",
            "stock_qty_min",
            "status",
            "needs_review",
            "condition",
            "can_be_sold",
            "private",
            "internal_part_number",
            "part_unit",
            "category",
            "storage",
            "footprint",
            "uuid",
            "comment",
            "production_remarks",
            "part_parameters_value",
            "distributors_sku",
            "manufacturers_sku",
            "part_attachments",
        )
