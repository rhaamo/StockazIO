# Generated by Django 3.1.3 on 2020-11-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_projectpart_sourced"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectpart",
            name="notes",
            field=models.CharField(blank=True, max_length=255, verbose_name="notes"),
        ),
    ]
