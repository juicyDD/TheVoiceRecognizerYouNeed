# Generated by Django 4.1.9 on 2023-05-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_alter_post_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.TextField(blank=True, null=True, verbose_name="Slug"),
        ),
    ]