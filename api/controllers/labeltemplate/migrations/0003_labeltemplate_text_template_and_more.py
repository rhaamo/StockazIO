# Generated by Django 4.0.2 on 2022-02-14 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labeltemplate", "0002_remove_labeltemplate_basepdf_labeltemplate_base_pdf"),
    ]

    operations = [
        migrations.AddField(
            model_name="labeltemplate",
            name="text_template",
            field=models.TextField(default="{name}\n\n{description}"),
        ),
        migrations.AlterField(
            model_name="labeltemplate",
            name="height",
            field=models.IntegerField(default=38, help_text="in mm"),
        ),
        migrations.AlterField(
            model_name="labeltemplate",
            name="width",
            field=models.IntegerField(default=90, help_text="in mm"),
        ),
    ]