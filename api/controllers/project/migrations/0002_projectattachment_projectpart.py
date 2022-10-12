# Generated by Django 3.1.3 on 2020-11-18 12:18

import django.db.models.deletion
from django.db import migrations, models

import controllers.part.validators


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0018_auto_20201118_1139"),
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectPart",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("part_name", models.CharField(blank=True, max_length=255, verbose_name="part name")),
                ("qty", models.IntegerField(default=1, verbose_name="part quantity")),
                (
                    "part",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="part.part"
                    ),
                ),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="project.project")),
            ],
        ),
        migrations.CreateModel(
            name="ProjectAttachment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "description",
                    models.CharField(
                        help_text="Description of the attachment", max_length=100, verbose_name="description"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="File to upload",
                        upload_to="part_attachments/",
                        validators=[controllers.part.validators.validate_file_type],
                        verbose_name="File",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_attachments",
                        to="project.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Attachment",
                "verbose_name_plural": "Project Attachments",
                "ordering": ("id",),
            },
        ),
    ]
