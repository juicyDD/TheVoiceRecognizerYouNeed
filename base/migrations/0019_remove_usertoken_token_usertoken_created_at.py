# Generated by Django 4.1.9 on 2023-06-16 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0018_usertoken"),
    ]

    operations = [
        migrations.RemoveField(model_name="usertoken", name="token",),
        migrations.AddField(
            model_name="usertoken",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]