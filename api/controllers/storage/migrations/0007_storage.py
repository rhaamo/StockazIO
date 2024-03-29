# Generated by Django 4.1.1 on 2022-10-11 15:40

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0006_alter_storagelocation_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Storage",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("description", models.CharField(blank=True, max_length=255, verbose_name="description")),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        help_text="Storage location",
                        null=True,
                        upload_to="storage_locations/",
                        verbose_name="Storage location pictures",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="storage.storage",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "storage location",
                "verbose_name_plural": "storage locations",
                "ordering": ("name",),
            },
        ),
    ]
