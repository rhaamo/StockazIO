from rest_framework import serializers
from .models import Distributor


class DistributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ["id", "name"]
