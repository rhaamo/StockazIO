from rest_framework import serializers

from .models import Distributor, DistributorSku


class DistributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ["id", "name", "address", "url", "email", "comment", "phone", "fax", "datasheet_url"]


class DistributorSkuSerializer(serializers.ModelSerializer):
    distributor = DistributorsSerializer(many=False, read_only=True)

    class Meta:
        model = DistributorSku
        fields = ["id", "sku", "part", "distributor", "datasheet_url"]


class DistributorSkuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorSku
        fields = ["id", "sku", "part", "distributor", "datasheet_url"]
