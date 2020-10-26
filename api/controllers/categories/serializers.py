from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
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
