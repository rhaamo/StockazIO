# Generated by Django 3.1.3 on 2020-11-19 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_projectpart_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="ibom_url",
            field=models.URLField(blank=True, verbose_name="ibom url"),
        ),
    ]
