# Generated by Django 3.0.1 on 2019-12-30 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0010_auto_20191230_1302"),
        ("distributor", "0002_distributorsku"),
    ]

    operations = [
        migrations.AlterField(
            model_name="distributorsku",
            name="distributor",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="parts_distributors_sku",
                to="distributor.Distributor",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="distributorsku",
            name="part",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, related_name="distributors_sku", to="part.Part"
            ),
            preserve_default=False,
        ),
    ]
