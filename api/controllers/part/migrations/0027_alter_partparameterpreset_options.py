# Generated by Django 4.1.1 on 2022-09-26 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0026_partattachment_picture_default"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="partparameterpreset",
            options={"ordering": ("name",)},
        ),
    ]
