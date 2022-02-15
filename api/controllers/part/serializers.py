from rest_framework import serializers
from .models import (
    ParametersUnit,
    PartUnit,
    Part,
    PartParameter,
    PartAttachment,
    PartStockHistory,
    PartParameterPreset,
    PartParameterPresetItem,
)
from django.conf import settings

from controllers.storage.serializers import StorageLocationSerializer
from controllers.categories.serializers import SingleCategorySerializer
from controllers.footprints.serializers import FootprintSerializer
from controllers.distributor.serializers import DistributorSkuSerializer, DistributorSkuCreateSerializer
from controllers.manufacturer.serializers import PartManufacturerSerializer, PartManufacturerCreateSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from controllers.upload_validator import FileTypeValidator


class ParametersUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametersUnit
        fields = ("id", "name", "symbol", "description")


class PartsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnit
        fields = ("id", "name", "short_name", "description")


class PartStockHistory(serializers.ModelSerializer):
    class Meta:
        model = PartStockHistory
        fields = ("id", "diff", "created_at")


class PartSerializer(serializers.ModelSerializer):
    storage = StorageLocationSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)
    part_stock_history = PartStockHistory(many=True, read_only=True)

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
            "created_at",
            "updated_at",
            "part_stock_history",
        )


class PartParameterSerializer(serializers.ModelSerializer):
    unit = ParametersUnitSerializer(many=False)

    class Meta:
        model = PartParameter
        fields = ("id", "name", "description", "value", "unit")


class PartParameterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartParameter
        fields = ("id", "name", "description", "value", "unit")


class PartAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    picture = serializers.ImageField()
    picture_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = PartAttachment
        fields = ("id", "description", "file", "file_size", "file_type", "picture", "picture_medium")


class PartAttachmentCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        required=False, validators=[FileTypeValidator(allowed_types=settings.PART_ATTACHMENT_ALLOWED_FILES)]
    )
    picture = serializers.FileField(
        required=False, validators=[FileTypeValidator(allowed_types=settings.PART_ATTACHMENT_ALLOWED_IMAGES)]
    )
    part = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all())

    class Meta:
        model = PartAttachment
        fields = ("id", "description", "file", "part", "picture")


class PartCreateSeralizer(WritableNestedModelSerializer):
    part_parameters_value = PartParameterCreateSerializer(many=True, required=False)
    manufacturers_sku = PartManufacturerCreateSerializer(many=True, required=False)
    distributors_sku = DistributorSkuCreateSerializer(many=True, required=False)
    part_attachments = PartAttachmentSerializer(many=True, required=False)

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
            "manufacturers_sku",
            "distributors_sku",
            "part_attachments",
        )


class PartRetrieveSerializer(serializers.ModelSerializer):
    storage = StorageLocationSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)
    part_parameters_value = PartParameterSerializer(many=True, read_only=True)
    distributors_sku = DistributorSkuSerializer(many=True, read_only=True)
    manufacturers_sku = PartManufacturerSerializer(many=True, read_only=True)
    part_attachments = PartAttachmentSerializer(many=True, read_only=True)
    part_stock_history = PartStockHistory(many=True, read_only=True)

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
            "created_at",
            "updated_at",
            "part_stock_history",
        )


class PartParametersPresetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartParameterPresetItem
        fields = ("id", "name", "description", "unit")


class PartParametersPresetSerializer(WritableNestedModelSerializer):
    part_parameters_presets = PartParametersPresetItemSerializer(many=True, read_only=False)

    class Meta:
        model = PartParameterPreset
        fields = ("id", "name", "part_parameters_presets")


class PartParametersPresetItemRetrieveSerializer(serializers.ModelSerializer):
    unit = ParametersUnitSerializer(many=False, read_only=True)

    class Meta:
        model = PartParameterPresetItem
        fields = ("id", "name", "description", "unit")


class PartParametersPresetRetrieveSerializer(WritableNestedModelSerializer):
    part_parameters_presets = PartParametersPresetItemRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = PartParameterPreset
        fields = ("id", "name", "part_parameters_presets")
