from rest_framework import serializers
from controllers.storage.models import StorageCategory, StorageLocation, Storage
from drf_spectacular.utils import extend_schema_field


class StorageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageCategory
        fields = ["id", "name", "parent"]


class StorageLocationSerializer(serializers.ModelSerializer):
    picture_medium = serializers.ImageField(read_only=True)

    @extend_schema_field(serializers.CharField())
    def get_category_name(self, obj):
        return obj.category.name

    class Meta:
        model = StorageLocation
        fields = ["id", "name", "description", "picture", "picture_medium", "uuid", "category", "category_name"]


StorageLocationSerializer._declared_fields["category_name"] = serializers.SerializerMethodField()


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
