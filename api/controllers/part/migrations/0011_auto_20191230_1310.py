# Generated by Django 3.0.1 on 2019-12-30 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0010_auto_20191230_1302"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partparameter",
            name="part",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="part_parameters_value",
                to="part.Part",
            ),
            preserve_default=False,
        ),
    ]
