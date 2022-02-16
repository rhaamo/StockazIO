import magic
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_type(upload):
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_buffer(upload.file.read(1024), mime=True)

    # Raise validation error if uploaded file is not an acceptable form of media
    if (
        file_type not in settings.PART_ATTACHMENT_ALLOWED_FILES
        or file_type not in settings.PART_ATTACHMENT_ALLOWED_IMAGES
    ):
        raise ValidationError("File type not supported.")


def validate_file_type_file(upload):
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_buffer(upload.file.read(1024), mime=True)

    # Raise validation error if uploaded file is not an acceptable form of media
    if file_type not in settings.PART_ATTACHMENT_ALLOWED_FILES:
        raise ValidationError("File type not supported.")


def validate_file_type_image(upload):
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_buffer(upload.file.read(1024), mime=True)

    # Raise validation error if uploaded file is not an acceptable form of media
    if file_type not in settings.PART_ATTACHMENT_ALLOWED_IMAGES:
        raise ValidationError("File type not supported.")
