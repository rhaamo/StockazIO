# Generated by Django 4.1.1 on 2022-10-11 16:39

from django.db import migrations, models
import uuid


def create_uuid(apps, schema_editor):
    StorageCategory = apps.get_model("storage", "StorageCategory")
    for sc in StorageCategory.objects.all():
        sc.uuid = uuid.uuid4()
        sc.save()


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0007_storage"),
    ]

    operations = [
        migrations.AddField(
            model_name="storagecategory",
            name="uuid",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(code=create_uuid, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="storagecategory",
            name="uuid",
            field=models.UUIDField(editable=False, null=False),
        ),
    ]
