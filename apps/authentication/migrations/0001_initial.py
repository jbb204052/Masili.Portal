# Generated by Django 4.1.3 on 2022-11-21 14:05

import apps.authentication.helper
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                (
                    "accountType",
                    models.CharField(
                        choices=[
                            ["RESIDENT", "RESIDENT"],
                            ["ADMIN", "ADMIN"],
                            ["SUPERADMIN", "SUPERADMIN"],
                            ["GUEST", "GUEST"],
                        ],
                        default="GUEST",
                        max_length=20,
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="profile_pics/default.png",
                        storage=apps.authentication.helper.OverwriteStorage(),
                        upload_to="profile_pics",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
