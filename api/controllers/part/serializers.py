from rest_framework import serializers
from .models import ParametersUnit


class ParametersUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametersUnit
        fields = ("name", "symbol", "prefix", "description")

