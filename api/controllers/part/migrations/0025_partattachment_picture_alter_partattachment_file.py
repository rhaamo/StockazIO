# Generated by Django 4.0.2 on 2022-02-15 08:21

import controllers.part.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0024_partattachment_file_size_partattachment_file_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="partattachment",
            name="picture",
            field=models.FileField(
                blank=True,
                help_text="Picture to upload",
                null=True,
                upload_to="part_attachments/",
                validators=[controllers.part.validators.validate_file_type_image],
                verbose_name="Picture",
            ),
        ),
        migrations.AlterField(
            model_name="partattachment",
            name="file",
            field=models.FileField(
                blank=True,
                help_text="File to upload",
                null=True,
                upload_to="part_attachments/",
                validators=[controllers.part.validators.validate_file_type_file],
                verbose_name="File",
            ),
        ),
    ]