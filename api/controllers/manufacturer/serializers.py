from rest_framework import serializers
from .models import Manufacturer, PartManufacturer, ManufacturerLogo


class ManufacturerLogoSerializer(serializers.ModelSerializer):
    logo_mini = serializers.ImageField(read_only=True)
    logo_small = serializers.ImageField(read_only=True)
    logo_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = ManufacturerLogo
        fields = ["logo", "logo_mini", "logo_small", "logo_medium"]


class ManufacturersSerializer(serializers.ModelSerializer):
    logos = ManufacturerLogoSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacturer
        fields = ["id", "name", "address", "url", "email", "comment", "phone", "fax", "logos"]


class PartManufacturerSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer(many=False)

    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer"]


class PartManufacturerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer"]
