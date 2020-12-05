# Generated by Django 3.1.3 on 2020-12-05 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("distributor", "0006_auto_20201114_1635"),
    ]

    operations = [
        migrations.AddField(
            model_name="distributor",
            name="datasheet_url",
            field=models.URLField(blank=True, max_length=255, verbose_name="Datasheet URL"),
        ),
        migrations.AddField(
            model_name="distributorsku",
            name="datasheet_url",
            field=models.URLField(blank=True, max_length=255, verbose_name="Datasheet URL"),
        ),
    ]
