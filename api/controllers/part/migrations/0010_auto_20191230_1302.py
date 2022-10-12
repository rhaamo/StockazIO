# Generated by Django 3.0.1 on 2019-12-30 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0009_auto_20191229_0756"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="part",
            options={"ordering": ("name",), "verbose_name": "part", "verbose_name_plural": "parts"},
        ),
        migrations.AlterField(
            model_name="partattachment",
            name="part",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="part_attachments",
                to="part.Part",
            ),
        ),
        migrations.AlterField(
            model_name="partparameter",
            name="part",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="part_parameter_values",
                to="part.Part",
            ),
        ),
    ]
