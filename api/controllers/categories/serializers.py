from rest_framework import serializers
from .models import Category
from controllers.utils import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    def get_parts_count(self, obj):
        return obj.parts_count

    def __init__(self, *args, depth=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = depth

    class Meta:
        model = Category
        fields = ["id", "name", "parts_count", "children"]

    def get_fields(self):
        fields = super().get_fields()
        if self.depth != 1:
            fields["children"] = RecursiveField(many=True, required=False)
        return fields


CategorySerializer._declared_fields["parts_count"] = serializers.SerializerMethodField()


CategorySerializer._declared_fields["children"] = CategorySerializer(
    many=True,
    source="get_children",
)


class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
