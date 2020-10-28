from rest_framework import serializers
from .models import Manufacturer, PartManufacturer


class ManufacturersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["id", "name"]


class PartManufacturerSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer(many=False, read_only=True)

    class Meta:
        model = PartManufacturer
        fields = ["id", "sku", "part", "manufacturer"]
