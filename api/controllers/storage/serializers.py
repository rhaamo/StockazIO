from rest_framework import serializers
from .models import StorageCategory, StorageLocation


class StorageLocationSerializer(serializers.ModelSerializer):
    picture_medium = serializers.ReadOnlyField(source="picture_medium.url")

    class Meta:
        model = StorageLocation
        fields = ['name', 'description', 'picture', 'picture_medium', 'uuid']


class StorageSerializer(serializers.ModelSerializer):
    storage_locations = StorageLocationSerializer(many=True, read_only=True)

    class Meta:
        model = StorageCategory
        fields = ["id", "name", "children", "storage_locations"]


StorageSerializer._declared_fields["children"] = StorageSerializer(many=True, source="get_children",)
