from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from controllers.categories.serializers import SingleCategorySerializer
from controllers.distributor.serializers import DistributorSkuCreateSerializer, DistributorSkuSerializer
from controllers.footprints.serializers import FootprintSerializer
from controllers.manufacturer.serializers import PartManufacturerCreateSerializer, PartManufacturerSerializer
from controllers.part.models import (
    ParametersUnit,
    Part,
    PartAttachment,
    PartParameter,
    PartParameterPreset,
    PartParameterPresetItem,
    PartStockHistory,
    PartUnit,
)

from controllers.storage.serializers import StorageSerializer
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


class PartAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    picture = serializers.ImageField()
    picture_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = PartAttachment
        fields = ("id", "description", "file", "file_size", "file_type", "picture", "picture_medium", "picture_default")


class PartSerializer(serializers.ModelSerializer):
    storage = StorageSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)
    part_stock_history = PartStockHistory(many=True, read_only=True)
    part_attachments = PartAttachmentSerializer(many=True, read_only=True)

    @extend_schema_field(serializers.CharField())
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    @extend_schema_field(serializers.CharField())
    def get_storage_path(self, obj):
        return obj.storage.full_path() if obj.storage else []

    @extend_schema_field(serializers.CharField())
    def get_category_path(self, obj):
        return obj.category.full_path() if obj.category else []

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
            "category_name",
            "category_path",
            "storage",
            "storage_path",
            "footprint",
            "uuid",
            "comment",
            "production_remarks",
            "created_at",
            "updated_at",
            "part_stock_history",
            "part_attachments",
        )


PartSerializer._declared_fields["category_name"] = serializers.SerializerMethodField()
PartSerializer._declared_fields["category_path"] = serializers.SerializerMethodField()
PartSerializer._declared_fields["storage_path"] = serializers.SerializerMethodField()


class PartParameterSerializer(serializers.ModelSerializer):
    unit = ParametersUnitSerializer(many=False)

    class Meta:
        model = PartParameter
        fields = ("id", "name", "description", "value", "unit")


class PartParameterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartParameter
        fields = ("id", "name", "description", "value", "unit")


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
    storage = StorageSerializer(many=False, read_only=True)
    category = SingleCategorySerializer(many=False, read_only=True)
    footprint = FootprintSerializer(many=False, read_only=True)
    part_unit = PartsUnitSerializer(many=False, read_only=True)
    part_parameters_value = PartParameterSerializer(many=True, read_only=True)
    distributors_sku = DistributorSkuSerializer(many=True, read_only=True)
    manufacturers_sku = PartManufacturerSerializer(many=True, read_only=True)
    part_attachments = PartAttachmentSerializer(many=True, read_only=True)
    part_stock_history = PartStockHistory(many=True, read_only=True)

    @extend_schema_field(serializers.CharField())
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    @extend_schema_field(serializers.CharField())
    def get_storage_path(self, obj):
        return obj.storage.full_path() if obj.storage else []

    @extend_schema_field(serializers.CharField())
    def get_category_path(self, obj):
        return obj.category.full_path() if obj.category else []

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
            "category_name",
            "category_path",
            "storage",
            "storage_path",
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


PartRetrieveSerializer._declared_fields["category_name"] = serializers.SerializerMethodField()
PartRetrieveSerializer._declared_fields["storage_path"] = serializers.SerializerMethodField()
PartRetrieveSerializer._declared_fields["category_path"] = serializers.SerializerMethodField()


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
