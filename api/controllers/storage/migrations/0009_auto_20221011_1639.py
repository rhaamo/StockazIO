# Generated by Django 4.1.1 on 2022-10-11 16:39

import mptt
from mptt.templatetags.mptt_tags import get_cached_trees
from django.db import migrations

def handle_location(item, parent, apps):
    Storage = apps.get_model('storage', 'Storage')
    p = Storage.objects.filter(uuid=parent.uuid).first()
    s = Storage(parent=p, name=item.name, description=item.description, picture=item.picture, uuid=item.uuid)
    s.save()


def handle_category(item, apps):
    Storage = apps.get_model('storage', 'Storage')

    if not item.parent:
        s = Storage(parent=None, name=item.name, uuid=item.uuid)
        s.save()
    else:
        p = Storage.objects.filter(uuid=item.parent.uuid).first()
        s = Storage(parent=p, name=item.name, uuid=item.uuid)
        s.save()

    # loop children categories if any
    for child in item.children.all():
        handle_category(child, apps)

    # loop storage locations if any
    for child in item.storage_locations.all():
        handle_location(child, item, apps)


def transfer_storage(apps, schema_editor):
    """
    Transfer StorageCategory and StorageLocation to Storage
    """
    StorageCategory = apps.get_model('storage', 'StorageCategory')
    mptt.register(StorageCategory)
    storage_tree = StorageCategory.objects.all()
    storage_tree = get_cached_trees(storage_tree)

    for i in storage_tree:
        handle_category(i, apps)

class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0008_storagecategory_uuid"),
    ]

    operations = [
        migrations.RunPython(code=transfer_storage, reverse_code=migrations.RunPython.noop)
    ]