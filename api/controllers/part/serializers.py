from rest_framework import serializers
from .models import ParametersUnit, PartUnit, Part


class ParametersUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametersUnit
        fields = ("id", "name", "symbol", "prefix", "description")


class PartsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnit
        fields = ("id", "name", "short_name", "description")


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ("id", "name", "description", "stock_qty", "stock_qty_min", "status", "needs_review", "condition", "can_be_sold", "private", "internal_part_number", "part_unit", "category", "storage", "footprint", "uuid", "comment", "production_remarks")
