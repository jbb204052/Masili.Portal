# Generated by Django 4.1.3 on 2022-11-21 14:11

import apps.authentication.helper
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="profile_pics/default.jpg",
                storage=apps.authentication.helper.OverwriteStorage(),
                upload_to=None,
            ),
        ),
    ]