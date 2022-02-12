from rest_framework import serializers
from .models import StorageCategory, StorageLocation
from controllers.utils import RecursiveField


class StorageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageCategory
        fields = ["id", "name", "parent"]


class StorageLocationSerializer(serializers.ModelSerializer):
    # picture_medium = serializers.ImageField(read_only=False)

    class Meta:
        model = StorageLocation
        fields = [
            "id",
            "name",
            "description",
            "picture",
            # "picture_medium",
            "uuid",
            "category",
        ]


class StorageSerializer(serializers.ModelSerializer):
    storage_locations = StorageLocationSerializer(many=True, read_only=True)

    def __init__(self, *args, depth=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = depth

    class Meta:
        model = StorageCategory
        fields = ["id", "name", "children", "storage_locations", "parent"]

    def get_fields(self):
        fields = super().get_fields()
        if self.depth != 1:
            fields["children"] = RecursiveField(many=True, required=False)
        return fields


StorageSerializer._declared_fields["children"] = StorageSerializer(
    many=True,
    source="get_children",
)
