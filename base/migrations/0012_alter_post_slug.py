# Generated by Django 4.1.9 on 2023-05-27 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_alter_post_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.FilePathField(blank=True, null=True, verbose_name="Slug"),
        ),
    ]