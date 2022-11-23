# Generated by Django 3.2.16 on 2022-11-23 20:45

import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dictionary",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "word",
                    models.CharField(max_length=250, unique=True, verbose_name="word"),
                ),
                ("frequency", models.PositiveBigIntegerField(default=0)),
                ("phonetics", models.JSONField(default=dict)),
                ("meanings", models.JSONField(default=dict)),
                ("license", models.JSONField(default=dict)),
                (
                    "source_urls",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.TextField(),
                        blank=True,
                        size=None,
                        verbose_name="source urls",
                    ),
                ),
            ],
            options={
                "verbose_name": "dictionary",
                "verbose_name_plural": "dictionary",
                "ordering": ("-frequency",),
            },
        ),
        migrations.CreateModel(
            name="Paragraph",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("para_content", models.TextField(verbose_name="Paragraph Content")),
            ],
            options={
                "verbose_name": "paragraph",
                "verbose_name_plural": "paragraphs",
                "ordering": ("-created_at",),
            },
        ),
    ]