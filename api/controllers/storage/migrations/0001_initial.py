# Generated by Django 3.0.1 on 2019-12-28 15:10

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StorageCategory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="storage.StorageCategory",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "storage categories",
            },
        ),
        migrations.CreateModel(
            name="StorageLocation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
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
                (
                    "category",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="storage.StorageCategory"
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
