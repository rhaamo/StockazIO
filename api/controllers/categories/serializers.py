from rest_framework import serializers
from .models import Category
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    @extend_schema_field(serializers.IntegerField())
    def get_parts_count(self, obj):
        return obj.parts_count

    class Meta:
        model = Category
        fields = ["id", "name", "parts_count", "children"]


CategorySerializer._declared_fields["parts_count"] = serializers.SerializerMethodField()

CategorySerializer._declared_fields["children"] = CategorySerializer(
    many=True,
    source="get_children",
)


class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
