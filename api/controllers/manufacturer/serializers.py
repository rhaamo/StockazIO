from rest_framework import serializers
from .models import Manufacturer


class ManufacturersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["id", "name"]
