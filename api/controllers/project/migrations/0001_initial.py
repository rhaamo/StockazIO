# Generated by Django 3.1.3 on 2020-11-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("description", models.TextField(blank=True, verbose_name="description")),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                ("ibom_url", models.URLField(verbose_name="ibom url")),
                (
                    "state",
                    models.IntegerField(
                        choices=[
                            (1, "Planned"),
                            (2, "Ongoing"),
                            (3, "Finished"),
                            (4, "Waiting"),
                            (5, "Abandonned"),
                            (99, "Unknown"),
                        ],
                        default=99,
                        verbose_name="state",
                    ),
                ),
                ("public", models.BooleanField(default=False, verbose_name="public")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
