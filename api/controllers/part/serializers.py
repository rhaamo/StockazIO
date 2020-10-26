from rest_framework import serializers
from .models import ParametersUnit, PartUnit


class ParametersUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametersUnit
        fields = ("name", "symbol", "prefix", "description")

class PartsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUnit
        fields = ("name", "short_name", "description")
