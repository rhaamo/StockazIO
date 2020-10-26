from rest_framework import serializers
from .models import FootprintCategory, Footprint


class FootprintSerializer(serializers.ModelSerializer):
    picture_mini = serializers.ReadOnlyField(source="picture_mini.url")
    picture_small = serializers.ReadOnlyField(source="picture_small.url")
    picture_medium = serializers.ReadOnlyField(source="picture_medium.url")

    class Meta:
        model = Footprint
        fields = ("id", "name", "picture", "picture_mini", "picture_small", "picture_medium", "description",)


class FootprintCategorySerializer(serializers.ModelSerializer):
    footprint_set = FootprintSerializer(many=True, read_only=True)

    class Meta:
        model = FootprintCategory
        fields = ["id", "name", "description", "footprint_set"]
