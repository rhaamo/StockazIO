# Generated by Django 4.0.2 on 2022-02-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0025_partattachment_picture_alter_partattachment_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="partattachment",
            name="picture_default",
            field=models.BooleanField(default=False),
        ),
    ]