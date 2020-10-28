from rest_framework import serializers
from .models import Distributor, DistributorSku


class DistributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ["id", "name"]


class DistributorSkuSerializer(serializers.ModelSerializer):
    distributor = DistributorsSerializer(many=False, read_only=True)

    class Meta:
        model = DistributorSku
        fields = ["id", "sku", "part", "distributor"]
