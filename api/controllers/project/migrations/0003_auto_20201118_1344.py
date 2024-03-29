# Generated by Django 3.1.3 on 2020-11-18 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_projectattachment_projectpart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectpart",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="project_parts", to="project.project"
            ),
        ),
    ]
