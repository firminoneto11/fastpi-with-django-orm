# Generated by Django 4.2.7 on 2023-12-24 23:14

from django.db import migrations, models

import shared.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("pk_id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "id",
                    models.CharField(
                        default=shared.utils.generate_uuid, max_length=36, unique=True
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
    ]
