# Generated by Django 3.0.1 on 2019-12-30 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0010_auto_20191230_1302"),
        ("manufacturer", "0002_partmanufacturer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partmanufacturer",
            name="part",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="manufacturers_sku",
                to="part.Part",
            ),
        ),
    ]
