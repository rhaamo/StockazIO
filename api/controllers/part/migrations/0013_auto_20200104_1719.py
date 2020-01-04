# Generated by Django 3.0.1 on 2020-01-04 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0012_auto_20191230_2127"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partattachment",
            name="description",
            field=models.CharField(
                help_text="Description of the attachment", max_length=100, verbose_name="description"
            ),
        ),
        migrations.AlterField(
            model_name="partattachment",
            name="part",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, related_name="part_attachments", to="part.Part"
            ),
            preserve_default=False,
        ),
    ]
