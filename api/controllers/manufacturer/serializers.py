from rest_framework import serializers
from controllers.manufacturer.models import Manufacturer, PartManufacturer, ManufacturerAlias
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ManufacturersAliasSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManufacturerAlias
        fields = ("id", "alias")


class ManufacturersSerializer(serializers.ModelSerializer):
    logo_mini = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)

    parts_manufacturers_alias = ManufacturersAliasSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacturer
        fields = [
            "id",
            "name",
            "address",
            "url",
            "email",
            "comment",
            "phone",
            "fax",
            "logo",
            "logo_mini",
            "logo_small",
            "logo_medium",
            "datasheet_url",
            "parts_manufacturers_alias"
        ]


class ManufacturersCreateSerializer(WritableNestedModelSerializer):
    logo_mini = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)

    parts_manufacturers_alias = ManufacturersAliasSerializer(many=True, required=False)

    class Meta:
        model = Manufacturer
        fields = [
            "id",
            "name",
            "address",
            "url",
            "email",
            "comment",
            "phone",
            "fax",
            "logo",
            "logo_mini",
            "logo_small",
            "logo_medium",
            "datasheet_url",
            "parts_manufacturers_alias"
        ]

class PartManufacturerSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer(many=False)

    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer", "datasheet_url"]


class PartManufacturerCreateSerializer(serializers.ModelSerializer):

    parts_manufacturers_alias = ManufacturersAliasSerializer(many=True, required=False)

    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer", "datasheet_url", "parts_manufacturers_alias"]
