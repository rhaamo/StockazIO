from django.conf import settings
from rest_framework import serializers

from controllers.part.models import Part
from controllers.part.serializers import PartSerializer
from controllers.project.models import Project, ProjectAttachment, ProjectPart
from controllers.upload_validator import FileTypeValidator


class ProjectPartSerializer(serializers.ModelSerializer):
    part = PartSerializer(many=False, required=False)

    class Meta:
        model = ProjectPart
        fields = ("id", "part", "part_name", "qty", "sourced", "notes")


class ProjectPartStandaloneSerializer(serializers.ModelSerializer):
    part = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), required=False)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectPart
        fields = ("id", "part", "part_name", "qty", "sourced", "notes", "project")


class ProjectAttachmentsSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        validators=[
            FileTypeValidator(
                allowed_types=settings.PART_ATTACHMENT_ALLOWED_FILES + settings.PART_ATTACHMENT_ALLOWED_IMAGES
            )
        ]
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectAttachment
        fields = ("id", "description", "file", "project")


class ProjectAttachmentsCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        required=False,
        validators=[
            FileTypeValidator(
                allowed_types=settings.PART_ATTACHMENT_ALLOWED_FILES + settings.PART_ATTACHMENT_ALLOWED_IMAGES
            )
        ],
    )
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = ProjectAttachment
        fields = ("id", "description", "file", "project")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "notes",
            "ibom_url",
            "state",
            "state_notes",
            "public",
            "created_at",
            "project_parts",
            "project_attachments",
        )


class ProjectRetrieveSerializer(serializers.ModelSerializer):
    project_parts = ProjectPartSerializer(many=True, required=False)
    project_attachments = ProjectAttachmentsSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "notes",
            "ibom_url",
            "state",
            "state_notes",
            "public",
            "created_at",
            "project_parts",
            "project_attachments",
        )
