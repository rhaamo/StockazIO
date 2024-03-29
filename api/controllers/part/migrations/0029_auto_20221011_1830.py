# Generated by Django 4.1.1 on 2022-10-11 18:30

from django.db import migrations


def remap_storage_fk(apps, schema_editor):
    Part = apps.get_model("part", "Part")
    Storage = apps.get_model("storage", "Storage")

    for part in Part.objects.all():
        if part.storage:
            s = Storage.objects.filter(uuid=part.storage.uuid).first()
            part.new_storage = s
            part.save()


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0028_part_new_storage"),
    ]

    operations = [
        migrations.RunPython(code=remap_storage_fk, reverse_code=migrations.RunPython.noop),
    ]
