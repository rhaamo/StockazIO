# Generated by Django 4.1.1 on 2022-10-12 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0003_auto_20191228_1507"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="level",
        ),
        migrations.RemoveField(
            model_name="category",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="category",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="category",
            name="tree_id",
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="categories.category",
                verbose_name="parent",
            ),
        ),
    ]