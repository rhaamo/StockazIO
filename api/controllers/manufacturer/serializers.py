from rest_framework import serializers
from controllers.manufacturer.models import Manufacturer, PartManufacturer


class ManufacturersSerializer(serializers.ModelSerializer):
    logo_mini = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = [
            "id",
            "name",
            "aliases",
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
        ]


class PartManufacturerSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer(many=False)

    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer", "datasheet_url"]


class PartManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer", "datasheet_url"]
