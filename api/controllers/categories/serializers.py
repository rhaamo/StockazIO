from rest_framework import serializers
from .models import Category
from django.core.exceptions import ObjectDoesNotExist


# Solution from https://github.com/axnsan12/drf-yasg/issues/632#issuecomment-778634940
class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        depth = self.context.get("depth", 0)
        self.context["depth"] = depth + 1
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(value, context=self.context, depth=self.context["depth"])

        return serializer.data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Objeto {0} does not exists".format(Model().__class__.__name__))
        return instance


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, depth=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = depth

    def get_parts_count(self, obj):
        return obj.part_set.count()

    def get_fields(self):
        fields = super().get_fields()
        if self.depth != 1:
            fields["children"] = RecursiveField(many=True)
        fields["parts_count"] = serializers.SerializerMethodField()
        return fields

    class Meta:
        model = Category
        fields = ["id", "name", "children"]


class SingleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
