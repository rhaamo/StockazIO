# Generated by Django 4.1.1 on 2022-10-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manufacturer", "0014_delete_manufactureralias"),
    ]

    operations = [
        migrations.AddField(
            model_name="manufacturer",
            name="aliases",
            field=models.CharField(blank=True, help_text="Aliases", max_length=255, verbose_name="aliases"),
        ),
    ]