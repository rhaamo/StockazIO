# Generated by Django 4.1.1 on 2022-10-11 17:01

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("storage", "0009_auto_20221011_1639"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storage",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="storagecategory",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
