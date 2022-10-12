from rest_framework import serializers

from .models import Footprint, FootprintCategory


class FootprintSerializer(serializers.ModelSerializer):
    picture_mini = serializers.ImageField(read_only=True)
    picture_small = serializers.ImageField(read_only=True)
    picture_medium = serializers.ImageField(read_only=True)

    class Meta:
        model = Footprint
        fields = ("id", "name", "picture", "picture_mini", "picture_small", "picture_medium", "description", "category")


class FootprintCategoryTreeSerializer(serializers.ModelSerializer):
    """
    Footprints with categories
    """

    footprint_set = FootprintSerializer(many=True, read_only=True)

    class Meta:
        model = FootprintCategory
        fields = ["id", "name", "description", "footprint_set"]


class FootprintCategorySerializer(serializers.ModelSerializer):
    """
    Footprint categories
    """

    class Meta:
        model = FootprintCategory
        fields = ["id", "name", "description"]
