# Generated by Django 3.0.1 on 2019-12-28 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0007_parametersunit_partparameter"),
        ("manufacturer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartManufacturer",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sku", models.CharField(max_length=255, verbose_name="sku id")),
                (
                    "manufacturer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="parts_manufacturers_sku",
                        to="manufacturer.Manufacturer",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="manufacturers_sku",
                        to="part.Part",
                    ),
                ),
            ],
            options={
                "verbose_name": "Manufacturer",
                "verbose_name_plural": "Manufacturers",
                "ordering": ("sku",),
            },
        ),
    ]
