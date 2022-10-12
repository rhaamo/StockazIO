# Generated by Django 3.1.2 on 2020-11-04 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0014_auto_20201104_0943"),
        ("distributor", "0003_auto_20191230_1302"),
    ]

    operations = [
        migrations.AlterField(
            model_name="distributorsku",
            name="part",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="distributors_sku",
                to="part.part",
            ),
        ),
    ]
