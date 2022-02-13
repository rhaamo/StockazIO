from rest_framework import serializers
from .models import LabelTemplate


class LabelTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelTemplate
        fields = ["id", "name", "height", "weight", "base_pdf", "template"]
