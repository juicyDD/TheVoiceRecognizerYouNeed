# Generated by Django 4.1.9 on 2023-05-26 05:51

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1024, verbose_name="Post Title")),
                ("thumbnail", models.ImageField(upload_to="")),
                (
                    "body",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Content"
                    ),
                ),
                ("summary", models.TextField(verbose_name="Summary")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
