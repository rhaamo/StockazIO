# Generated by Django 3.1.3 on 2020-11-14 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("distributor", "0005_auto_20201114_1602"),
    ]

    operations = [
        migrations.AlterField(
            model_name="distributorsku",
            name="distributor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parts_distributors_sku",
                to="distributor.distributor",
            ),
        ),
    ]
