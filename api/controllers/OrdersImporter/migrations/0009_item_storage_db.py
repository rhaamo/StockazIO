# Generated by Django 5.1.4 on 2024-12-30 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("OrdersImporter", "0008_item_new_in_stock_item_part_db"),
        ("storage", "0011_remove_storagelocation_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="storage_db",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="storage.storage"
            ),
        ),
    ]
